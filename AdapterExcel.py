import openpyxl

from models import *


class Adapter_XLSX:
    def __init__(self, file_name):
        self.dict_data = {}
        self.generate_dict(file_name)
        #self.extract_data(self.dict_data)
        print self.dict_data

    def generate_dict(self, name_file):
        wb = openpyxl.load_workbook(name_file)
        self.dict_data = wb



    # def extract_data(self, dict_data):
    #     for i in dict_data:
    #         
    #     


ad = Adapter_XLSX('inventario_auge.xls')

