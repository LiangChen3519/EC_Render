from __future__ import annotations
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import pandas as pd


@dataclass
class BiometReshape:
    biomet_type: str
    site: str
    year: int
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
        '''
        a function to read biomet data based on the biomet sensor
        :return: a dataframe of biomet data based on the biomet type
        '''
        if self.biomet_type.lower() == "licor":
            self.licor_path = Path("data/{self.site}/{self.year}/{self.biomet_type.lower()}")
            if not self.licor_path.exists():
                os.makedirs(self.licor_path)
            self.biomet_data = self.read_licor()
        elif self.biomet_type.lower() == "cr3000":
            self.cr3000_path = Path("data/{self.site}/{self.year}/{self.cr3000_path.lower()}")
            if not self.cr3000_path.exists():
                os.makedirs(self.cr3000_path)
            self.biomet_data = self.read_cr3000()
        elif self.biomet_type.lower() == "fmi":
            self.fmi_path = Path("data/{self.site}/{self.year}/{self.fmi_path.lower()}")
            if not self.fmi_path.exists():
                os.makedirs(self.fmi_path)
            self.fmi_data = self.read_fmi(self.fmi_path)
        else:
            raise ValueError("Invalid biomet type at this moment")

    def read_licor(self):
       '''
       a function to read biomet data from licor Biomet sensor
       :param licor_path:
       :return: a dataframe of biomet data from Biomet sensor
       '''
       bio_licor = pd.read_csv(self.licor_path)
       return bio_licor


    def read_fmi(self):
        '''
        a function to read biomet data from FMI
        :param self: data path
        :param fmi_path: save path
        :return: a dataframe of biomet data from FMI
        '''
        bio_fmi = pd.read_csv(self.fmi_path)
        return bio_fmi


    def read_cr3000(self):
        '''
        a function to read biomet data from CR3000 campbell sensor
        :param self: data path
        :param cr3000_path: save path
        :return: a dataframe of biomet data from CR3000
        '''
        bio_cr3000 = pd.read_csv(self.cr3000_path)
        return bio_cr3000

    def reshapeBiometData(self):

        pass
