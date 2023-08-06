from tests.robot.src import IoC_Container
from tests.robot.src.passwordmanager.src.abstract.i_user_credentials import IUserCredentials


class DecryptXLData:
    """
    This is decrypt XL data class which is responsible for decrypt users credential
    © BRAIN STATION 23 | Design and Development: Md. Nur Amin Sifat (BS1131)
    """

    def __init__(self):
        self.ioc_container = IoC_Container.CONTAINER

    def get_all_user_decrypted_credentials(self):
        # get all user decrypted credentials
        user_cred_obj: IUserCredentials = self.ioc_container.resolve(IUserCredentials)
        return user_cred_obj.get_all_users()

    def get_specific_user_decrypted_credential(self, username: str):
        # get specific user's decrypted data
        user_cred_obj: IUserCredentials = self.ioc_container.resolve(IUserCredentials)
        return user_cred_obj.get_user_credentials_by_name(username)

