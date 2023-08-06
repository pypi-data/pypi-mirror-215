"""
© BRAIN STATION 23 | Design and Development: Md. Nur Amin Sifat (BS1131)
"""
from robot.src.abstract.menu import Menu
from robot.src import ObjMapper
from robot.src import IoC_Container
from testdata.xl.decrypt_xl_data import DecryptXLData


class ManageDecryption(Menu):
    """
    Manage Decryption is a manager which is responisble for providing the services
    of Decryption of user credentail according to the user request.
    © BRAIN STATION 23 | Design and Development: Md. Nur Amin Sifat (BS1131)
    """

    banner = '''
    ------------------------------------------------------------------------
    -------------------------- Decryption Manager---------------------------
    ------------------------------------------------------------------------ 
    '''
    option_menu = '''
    [1] Get all users decrypted credentials
    [2] Get specific users decrypted credentials
    [0] Exit
    '''

    def __init__(self) -> None:
        self.ioc_container = IoC_Container.CONTAINER
        self.obj = DecryptXLData()

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
                    print(self.obj.get_all_user_decrypted_credentials())
                case 2:
                    username = input("Enter username: ")
                    print(self.obj.get_specific_user_decrypted_credential(username))
                case _:
                    raise ValueError("Not an option")
        # After a Successful operation getting back to current Menu for further actions
        self.menu()

    def menu(self):
        self.display()
        choice = self.get_input()
        self.switch_options(choice)