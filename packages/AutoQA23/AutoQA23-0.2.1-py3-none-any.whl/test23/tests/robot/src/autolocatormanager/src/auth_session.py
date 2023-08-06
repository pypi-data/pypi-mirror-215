from typing import Any
from getpass import getpass
from bs4 import BeautifulSoup
from ..constants import Constants
from selenium.webdriver.support import wait
from .abstract.i_auth_session import IAuthSession
from ...autolocatormanager.constants import Constants
from tests.robot.src import log_file


class AuthSession(IAuthSession):
    

    def get_authenticated_driver(self, target_link: str, auth_credentials: dict = None, driver_obj: Any = None) -> dict:
        self._get_token(target_link, Constants.GENERAL_HTTP_HEADER, driver_obj)
        auth_credentials = self._input_auth_credentials()
        print(Constants.SESSION_DATA)
        cookies,target_link = self._create_auth_session(target_link, Constants.SESSION_DATA)
        return self.insert_cookies_in_driver(cookies, driver_obj),target_link


    def insert_cookies_in_driver(self, cookies: dict, driver_obj: Any) -> Any:
        for key in cookies:
            print(f"Cookie Name: {key} inserted.....")
            driver_obj.add_cookie({'name': key, 'value': cookies[key]})
            print(driver_obj)
        return driver_obj

    def _input_auth_credentials(self) -> dict:
        temp_value = input('Please, provide a valid user name: ')
        Constants.SESSION_DATA[Constants.AUTH_CREDENTIALS['user_field_name']] = temp_value
        temp_value = getpass('Please, provide a valid Password: ')
        Constants.SESSION_DATA[Constants.AUTH_CREDENTIALS['password_field_name']] = temp_value
        return Constants.SESSION_DATA

    def _driver_config(self, target_link: str, driver_obj: Any) -> dict:
        # =====> Hitting the URL 1st Time to Collect the value of cookies[name] = domain
        driver_obj.get(target_link)
        driver_obj.implicitly_wait(10)
        """
        The reason of two times hitting the link is: 
            - Selenium webdriver init with default url data:. 
            - add_cookie require current url is under the domain pattern of cookie. 
            - data: will not match any cookie domain
            Ref: https://itecnote.com/tecnote/python-selenium-chromedriver-add-cookie-invalid-domain-error/
        """
        
        
        msg =  f"Domain:{driver_obj.get_cookies()}"
        log_file.write_log(msg)
        

        driver_obj.implicitly_wait(10)
        # CSRF/XSRF Tokens
        token_name = driver_obj.find_element(
            "xpath", '//input[@type="hidden"]').get_attribute("name")
        token_value = driver_obj.find_element(
            "xpath", '//input[@type="hidden"]').get_attribute("value")
        print('token>>>>>',token_name,token_value)
        return {'token_name': token_name, 'token_value': token_value}

    def _update_const_cred(self, field_key: str, field_value) -> bool:
        try:
            Constants.AUTH_CREDENTIALS[field_key] = field_value
            print(
                f"AUTH_CREDENTIALS dictionary updated successfully. Dict key =>{field_key}<= updated with =>{field_value}<= as value.")
            return True
        except Exception:
            print(
                f"Something went wrong! AUTH_CREDENTIALS dictionary was not updated. Requested Dict key was =>{field_key}<= and the value was =>{field_value}<= .")
            return False

    def _get_token(self, target_link: str, header: dict, driver_obj: Any = None) -> dict:
        try:
            token_name: str
            if driver_obj is None:
                token_name = input(
                    "Please, inspect the targeted website and provide a valid token name: ")
            else:
                token_dict = self._driver_config(target_link, driver_obj)
                token_name = token_dict['token_name']
                self._update_const_cred(
                    field_key='token_name', field_value=token_name)
            response = self._session.get(target_link, headers=header)
            print(f"HTTP STATUS CODE (GET): {response.status_code}")
            # --- search fresh token in HTML ---
            soup = BeautifulSoup(response.text,'lxml')
            # Getting token value from the HTML input field.
            new_token = soup.find('input', {'name': token_name})['value']
            self._update_const_cred(
                field_key='token_value', field_value=new_token)
            Constants.SESSION_DATA[token_name] = new_token
            msg = f"Token Name:{token_name},Token Value:{new_token}"
            log_file.write_log(msg)
            return {token_name: new_token}
        except Exception as e:
            print(f"""
                   ==========>Something went wrong !<==========
                   HTTP GET request was not successful. 
                   Unable to collect the TOKEN!
                   ____________________________________________
                   # ERROR: {str(e)}
                   """)
            return {'error': str(e)}

    def _create_auth_session(self, target_link: str, auth_credentials: dict) -> dict:
        redirect_url = None
        
        while target_link!=redirect_url:
             auth_response = self._session.post(target_link, data=auth_credentials)
             cookies = self._session.cookies.get_dict()
             redirect_url = target_link
             target_link = auth_response.url
    
        
        msg =   f"Cookies:{cookies}"
        log_file.write_log(msg)
        
        print(f"Cookies:{cookies}")
        print(f"HTTP STATUS CODE (POST): {auth_response.status_code}")
        print(f"Dashboard Link:{target_link}")
        
        return cookies,target_link
