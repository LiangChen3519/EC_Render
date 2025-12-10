import re
from pathlib import Path
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.cm as cm


## ERA5 data is used for gapfilling the radiation data from CR3000
## or Biomet sensor
## weaather data should be collected from the weather station if is possible

class Era5Reshape:
    def __init__(self, era5_data:str):
        #  era5_data is the path to the era5 data
        self._era5_data = era5_data
        # begin_data is the first date of the year with format 2018-12-01T18:00:00
        # self._begin_date = begin_date # as datetime
        # we usually use the following variables
        self.var_names = ["stl1", "swvl1", "ssrd", "strd", "ssr", "str"]

        # check which month is missing from the data

    def checkMonth(self, grib_list:list) -> bool:
        flag = True
        monthFound = []
        if len(grib_list) != 12:
            for file in grib_list:
                m = file.stem.split("_")[2]
                m = int(m)
                monthFound.append(m)
            missingMonth = list(set(range(1, 13)) - set(monthFound))
            print(f"Missing months detected: {missingMonth}")
            flag = False
        return flag

        # get the begining date of a file

    def get_begin_date(self, filePath:Path) -> pd.Timestamp:
        filename = filePath.stem
        match = re.search(r"era5_(\d{4})_(\d{2})", filename)
        year, month = match.groups()
        # print(f"{year}-{month}")
        begin_date = pd.to_datetime(f"{year}-{month}-01 00:00:00")
        return begin_date

    def loadGrib(self, filePath:Path, shortName:str) -> xr.Dataset:
        # for var in self.var_names:
        ds = xr.open_dataset(filePath,
                             engine="cfgrib",
                             backend_kwargs={"filter_by_keys": {"shortName": shortName}})
        begin_date = self.get_begin_date(filePath)
        ds = ds.sel(time=slice(begin_date, None))  # cutting the data
        return ds

    def readGrib(self, filename:Path) -> pd.DataFrame:
        ds_list_radiation = []
        ds_list_soil = []
        for var in self.var_names:
            try:
                ds = self.loadGrib(filename, var)
                if var in ["stl1", "swvl1"]:
                    ds_list_soil.append(ds)
                else:
                    ds_list_radiation.append(ds)
            except:
                print(f"Error reading {filename} for variable {var}")
                continue
        ds_soil = xr.merge(ds_list_soil, compat='override')
        ds_radiation = xr.merge(ds_list_radiation, compat='override')
        df_soil = ds_soil.to_dataframe().reindex()
        df_radiation = ds_radiation.to_dataframe().reindex()
        df_soil = df_soil[["valid_time", "stl1", "swvl1"]]
        df_radiation = df_radiation[["valid_time", "ssrd", "strd", "ssr", "str"]]
        df = pd.merge(df_radiation,
                      df_soil,
                      on="valid_time",
                      how='outer')
        #df.index = pd.to_datetime(df.valid_time)

        # keep all time period from day1 to day365/366
        return df

    def reshapeEra5Data(self) -> pd.DataFrame:
        grib_list = list(Path(self._era5_data).glob("*.grib"))
        all_data = []
        # a year should have 12 files (monthly data)
        if self.checkMonth(grib_list):
            print("Data is missing for some months")
            # return None
            # read the grib data but divide into 2 parts
            # 1st into soil
            # 2nd into radiation part
        for file in grib_list:
            print(f"Reading {file} ...")
            df = self.readGrib(filename=file)
            all_data.append(df)
        final_df = pd.concat(all_data, ignore_index=True)
        print("all files are done...")
        return final_df

    def resampleERA5(self,df:pd.DataFrame,resample_freq:str="30min") -> pd.DataFrame:
        # assign a time index
        df.index = pd.to_datetime(df.valid_time)
        df.drop(["valid_time"], axis=1, inplace=True) # remove the duplicate column
        # conver to the unit to w/m2 for radiations
        df[["ssrd", "strd", "ssr", "str"]] = df[["ssrd", "strd", "ssr", "str"]].divide(3600)
        # creat other variables ["NetRadiation","SW_out","LW_out","PPFD"]
        df["NetRadiation"] = df["ssr"] + df["str"]
        df["SW_out"] = df["ssrd"] - df["ssr"]
        df["LW_out"] = df["strd"] - df["str"]
        df["PPFD"] = df["ssrd"] *2.04 # mu mol / m2 / s
        print("Now start plot ERA5 variable and save it as pdf........")

        cols = ["ssrd", "strd", "ssr", "str", "NetRadiation","SW_out","LW_out","PPFD","stl1", "swvl1"]
        colors = colors = cm.tab10.colors
        # create 2 rows × 3 columns of subplots
        fig, axes = plt.subplots(2, 5, figsize=(15, 6), sharex=True)
        # flatten axes (so we can loop easily)
        axes = axes.flatten()
        # plot each variable
        for i, col in enumerate(cols):
            axes[i].plot(df.index, df[col],color=colors[i])
            axes[i].set_title(col)
            axes[i].grid(True)
            axes[i].tick_params(axis='x', rotation=45)
        plt.tight_layout()
        plt.savefig("ERA5_resample_Variable.pdf")
        df = df[~df.index.duplicated(keep="first")]
        return df.resample(resample_freq).interpolate(method="linear")
