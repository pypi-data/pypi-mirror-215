"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
import os
from re import I
import sys
from os.path import dirname as up

from termcolor import colored
from tests.robot.src import ObjMapper
two_up = up(up(__file__))
# append the path of the parent directory
sys.path.append(two_up)
from tests.robot.src.abstract.menu import Menu
from .xl.xl_test_data import XLtestData
from tests.testdata.managexldata.manage_encryption_data import ManageEncryption
from tests.testdata.managexldata.manage_decryption_data import ManageDecryption
from .xl.sample import Sample

class TestDataManager(Menu):

    banner = """
    ------------------------------------------------------------------------
    ------------------Data Set Manager (Data Driven Test) ------------------
    ------------------------------------------------------------------------ 
    """

    option_menu = '''
    [1] EXCEL 
    [2] Encrypt XL/CSV Data
    [3] Decrypt XL/CSV Data
    [4] Sample
    '''

    #Add the initialized objects here.
    OPTION_TYPES = {
        1: XLtestData(),
        2: ManageEncryption(),
        3: ManageDecryption(),
        4: Sample()
    }

    def __init__(self) -> None:
        self.get_indexed()

    def get_indexed(self):
        ObjMapper.OBJ_MAP['test_data_manager'] = ObjMapper.remember(self)

    def display(self):
        print(self.banner)
        print(self.option_menu)

    def get_input(self):
        option = int(input("Please, provide an integer input and press Enter!:"))
        return option

    def switch_options(self, choice: int):
        # data_set_obj = self.OPTION_TYPES[choice]
        #Open-Closed Principle
        #https://www.pythontutorial.net/python-oop/python-open-closed-principle/

        if (choice == 0):
            id = ObjMapper.OBJ_MAP['root_manager']
            route = ObjMapper.id2obj(id)
            route.menu()
            return None
        elif choice == 1:
            data_set_obj = self.OPTION_TYPES[choice]
            # Open-Closed Principle
            # https://www.pythontutorial.net/python-oop/python-open-closed-principle/
            print(colored(data_set_obj.arrange_data_set("vertical"),'red'))
            self.menu()
        else:
            #Getting sub menu object by option number.
            sub_menu_obj: Menu = self.OPTION_TYPES[choice]
            #Open-Closed Principle
            #https://www.pythontutorial.net/python-oop/python-open-closed-principle/
            sub_menu_obj.menu()
    
    def menu(self):
        self.display()
        choice = self.get_input()
        self.switch_options(choice)