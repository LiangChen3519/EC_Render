import DataLoader
import Era5Reshape
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    site = "yla"
    year = 2019
    out_path = f"./data/{site}/{year}/ERA5"
    # dl = DataLoader.DataLoader(site,year,out_path)
    # dl.download()
    # beginning = pd.to_datetime(f"{year}-01-01 00:00:00")
    er = Era5Reshape.Era5Reshape(out_path)
    final_ds = er.reshapeEra5Data()
    final_ds = er.resampleERA5(final_ds)  # resample to 30min
    final_ds.to_csv(f"{out_path}/{site}_{year}_ERA5_GRIB_HH.csv", index=True, encoding="utf-8")
