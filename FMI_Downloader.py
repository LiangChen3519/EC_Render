# we delay this part, since i found that direct download form the FMI webpage is
# more easy that run a script
# so this class is delay and further check will be done in the main file

import datetime as dt
from fmiopendata.wfs import download_stored_query
from __future__ import annotations
from setting import SITE_AREA

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import pandas as pd

@dataclass
class FMI_Downloader:
    year: int
    site: str
    bbox: list


    def download(self):
        start_date = dt.datetime(self.year, 1, 1).strftime('%Y-%m-%dT00:00:00Z')
        end_date = dt.datetime(self.year, 12, 31).strftime('%Y-%m-%dT23:59:59Z')
        if self.site not in SITE_AREA.keys():
            raise ValueError(f"site {self.site} is invalid")
        self.bbox = SITE_AREA[self.site]