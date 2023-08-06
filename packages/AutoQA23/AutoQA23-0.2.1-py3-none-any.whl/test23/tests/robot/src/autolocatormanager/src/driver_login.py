import time
import os
from getpass import getpass
from ..constants import Constants
from selenium.webdriver.support import wait
from .abstract.i_auth_scraping import IAuthScraping
from selenium.webdriver.common.by import By

from typing import Any

from dotenv import load_dotenv

load_dotenv()

class DriverLogin(IAuthScraping):

    def get_authenticated_driver(self, target_link: str, auth_credentials: dict = None, driver_obj: Any = None) -> Any:
        driver_obj.get(target_link)
        driver_obj.get(driver_obj.current_url)
        get_username_field = os.getenv('USERNAME_FIELD') if os.getenv('USERNAME_FIELD') is not None else input("enter username field name: ")
        username = driver_obj.find_element(By.NAME, get_username_field)
        username_value = os.getenv('USERNAME_VALUE') if os.getenv('USERNAME_VALUE') is not None else input("enter username: ")
        username.send_keys(username_value)
        time.sleep(2)
        submit_button = driver_obj.find_element(By.NAME, "action")

        submit_button.click()
        time.sleep(2)
        password_field = os.getenv('PASSWORD_FIELD') if os.getenv('PASSWORD_FIELD') is not None else input("enter password field name: ")
        password = driver_obj.find_element(By.NAME, password_field)
        password_value = os.getenv('PASSWORD_VALUE') if os.getenv('PASSWORD_VALUE') is not None else getpass("enter password: ")
        password.send_keys(password_value)

        print("\npassword inserted done.......\n")

        submit_button = driver_obj.find_element(By.NAME, "action")
        submit_button.click()

        print("\nsubmit clicked done.......\n")

        time.sleep(2)
        print(driver_obj.current_url)

        return driver_obj
