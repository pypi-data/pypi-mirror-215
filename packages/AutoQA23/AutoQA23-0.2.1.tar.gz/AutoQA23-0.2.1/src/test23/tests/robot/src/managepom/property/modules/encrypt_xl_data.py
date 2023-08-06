from termcolor import colored
from tests.robot.src import IoC_Container
from tests.robot.src.passwordmanager.src.abstract.i_user_credentials import IUserCredentials


class EncryptXLData:
    """
    This is encrypt XL data class which is responsible for encrypt users credential
    © BRAIN STATION 23 | Design and Development: Md. Nur Amin Sifat (BS1131)
    """

    def __init__(self):
        self.ioc_container = IoC_Container.CONTAINER

    def __formate_multiple_user_credential(self, data: dict) -> dict:
        """
        Formate multiple user credential data, response will data = {'username':[username list],
        'password':[password list]} to data_dict = { 'username': password, ... }
        """
        data_dict = dict()
        try:
            for _username, _password in zip(data["username"], data["password"]):
                data_dict[_username] = _password
            return data_dict
        except Exception as e:
            print(colored(f"Invalid data form({str(e)})",'red'))

    def encrypt_user_credentials(self, _user_credentials: dict):
        # encrypt users credential which are get from XL
        user_cred_obj: IUserCredentials = self.ioc_container.resolve(IUserCredentials)
        # get formated user data
        multi_user_credential_data = self.__formate_multiple_user_credential(_user_credentials)
        # add multiple user credentials
        user_cred_obj.add_multiple_credentials(multi_user_credential_data)

    def get_all_users_data(self):
        # get all encrypted user credential
        user_cred_obj: IUserCredentials = self.ioc_container.resolve(IUserCredentials)
        return user_cred_obj.get_all_users(is_encrypted=True)
