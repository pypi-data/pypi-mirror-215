import os
from tests.robot.src import ObjMapper
from tests.robot.src.abstract.menu import Menu
from tests.robot.src.manager import RoboManager
from termcolor import colored
import logging
logger = logging.getLogger(__name__)



flag = False
testdata_manager_obj = None
def getCurrentOptions():
    global flag, testdata_manager_obj
    try:
        if testdata_manager_obj is None:
            from tests.testdata.test_data_manager import TestDataManager
            testdata_manager_obj = TestDataManager()
            flag = True
        return testdata_manager_obj, flag
    except:
        logger.warning(colored("POM Structure Not created, Please create pom structure first",'red'))
        return testdata_manager_obj, flag


class Test23(Menu):
    """
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    test_manager_obj, flag_l = getCurrentOptions()
    #Add the initialized objects here.
    MANAGER_OPTIONS = {
        1: RoboManager(),
        2: test_manager_obj if flag_l else None,
    }
    
    banner = """
    -----------------------------------------------------------------------
    --------------------------------TEST-23--------------------------------
    -----------------------------------------------------------------------
    """
    
    option_menu = f"""
            [1] Robot
            [2] Data Manager
            [3] Exit
    """ if flag_l else """
            [1] Robot
            [3] Exit
    """

    def __init__(self):
        self.get_indexed()
        
        
    def get_indexed(self):
        ObjMapper.OBJ_MAP['root_manager'] = ObjMapper.remember(self) 
        

        
    def display(self):
        print(self.banner)
        print(self.option_menu)  
    
    def get_input(self):
        return super().get_input() 
    
    def switch_options(self, choice: int):
        if (choice == 0):
            print("=======================END=======================")
        else:
            manager = self.MANAGER_OPTIONS[choice]
            manager.menu()
            
    def menu(self):
        self.display()
        choice = self.get_input()
        self.switch_options(choice)

def main():
    print(os.path.dirname(__file__))
    try:
        test23 = Test23()
        test23.menu()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(__package__)
    main()