"""
© BRAIN STATION 23 | Design and Development: Md. Nur Amin Sifat (BS1131)
"""
from tests.robot.src.abstract.menu import Menu
from tests.robot.src import ObjMapper
from tests.robot.src import IoC_Container
from ..xl.encrypt_xl_data import EncryptXLData
from ..xl.xl_test_data import XLtestData


class ManageEncryption(Menu):
    """
    Manage Encryption is a manager which is responsible for providing the services
    of encryption of user credential according to the user request.
    © BRAIN STATION 23 | Design and Development: Md. Nur Amin Sifat (BS1131)
    """

    banner = '''
    ------------------------------------------------------------------------
    -------------------------- Encryption Manager---------------------------
    ------------------------------------------------------------------------ 
    '''
    option_menu = '''
    [1] Encrypted users credentials
    [2] Get all encrypted users credential
    [0] Exit
    '''

    def __init__(self) -> None:
        self.ioc_container = IoC_Container.CONTAINER
        self.obj = EncryptXLData()

    def get_indexed(self):
        return self.super().get_indexed(self)

    def display(self):
        print(self.banner)
        print(self.option_menu)

    def get_input(self):
        return super().get_input()

    def switch_options(self, choice: int):
        if choice == 0:
            id = ObjMapper.OBJ_MAP['test_data_manager']
            route = ObjMapper.id2obj(id)
            route.menu()
            return None
        else:
            match choice:
                case 1:
                    xl_user_data = XLtestData().arrange_data_set("vertical")
                    self.obj.encrypt_user_credentials(xl_user_data)
                case 2:
                    print(self.obj.get_all_users_data())
                case _:
                    raise ValueError("Not an option")
        # After a Successful operation getting back to current Menu for further actions
        self.menu()

    def menu(self):
        self.display()
        choice = self.get_input()
        self.switch_options(choice)