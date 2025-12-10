from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import pandas as pd


@dataclass
class BiometReshape:
    biomet_type: str
    licor_path: Optional[Path] = None
    cr3000_path: Optional[Path] = None
    fmi_path: Optional[Path] = None
    # different dataframe
    biomet_data: Optional[pd.DataFrame] = field(default=None, init=False)
    fmi_data: Optional[pd.DataFrame] = field(default=None, init=False)
    era_data: Optional[pd.DataFrame] = field(default=None, init=False)
    merged_data: Optional[pd.DataFrame] = field(default=None, init=False)

    # read biomet data
    def readBiomet(self):
        if self.biomet_type.lower() == "licor":
            self.biomet_data = self.read_licor(self.licor_path)
        elif self.biomet_type.lower() == "cr3000":
            self.biomet_data = self.read_cr3000(self.cr3000_path)
        elif self.biomet_type.lower() == "fmi":
            self.fmi_data = self.read_fmi(self.fmi_path)
        else:
            raise ValueError("Invalid biomet type")

    def read_licor(self, licor_path:Path):
        pass


    def read_fmi(self, fmi_path:Path):
        pass


    def read_cr3000(self, cr3000_path):
        pass
