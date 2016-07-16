import pyexcel as pe
import pyexcel.ext.xlsx
from .. import models

class Adapter_XLSX:
    def __init__(self, dict_data):
        self.dict_data = dict_data
        self.extract_data(self.dict_data)

    # def extract_data(self, dict_data):
    #     for i in dict_data:
    #         
    #     

# records = pe.get_records(file_name='inventory.xlsx')
