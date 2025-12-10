import os
import cdsapi
from setting import SITE_AREA

class DataLoader:
    def __init__(self, site, year, output_path):
        if site not in SITE_AREA.keys():
            raise ValueError(f"site {site} is not supported")
        self._site = site
        self._year = year
        self._output_path = output_path
        self.area = SITE_AREA[site]
        # check the output path
        os.makedirs(self._output_path, exist_ok=True)

    # download data
    def download(self):
        variables = [
            "surface_net_solar_radiation",
            "surface_net_thermal_radiation",
            "surface_solar_radiation_downwards",
            "surface_thermal_radiation_downwards",
            "soil_temperature_level_1",
            "volumetric_soil_water_layer_1",
        ]

        client = cdsapi.Client()
        # Loop through months
        for month in range(1, 13):
            request = {
                "product_type": ["reanalysis"],
                "variable": variables,
                "year": self._year,
                "month": f"{month:02d}",
                "day": [f"{d:02d}" for d in range(1, 32)],
                "time": [f"{h:02d}:00" for h in range(24)],
                "data_format": "grib",
                "download_format": "unarchived",
                "area": self.area,
            }

            filename = os.path.join(self._output_path, f"era5_{self._year}_{month:02d}_{self._site}.grib")
            print(f"Downloading {filename} ...")
            client.retrieve("reanalysis-era5-single-levels",
                            request,
                            target=filename)
