import os
import imp
import sys
import time
import inspect
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support import wait
from ... import IoC_Container
from bs4 import BeautifulSoup
from termcolor import colored

from .abstract.i_scraper import IScraper

from .abstract.i_auth_scraping import IAuthScraping

from .driver_login import DriverLogin
from .auth_session import AuthSession

from ... import ObjMapper
import pickle
from ..constants import Constants
from tests.robot.src import log_file

# from tests.drivercontroller.driver_factory import DriverFactory

driver_factory_obj = None
constants_obj = None
driver_g = None


def getDriver():
    try:
        global driver_factory_obj, constants_obj, driver_g
        if driver_g is None:
            from tests.drivercontroller.driver_factory import DriverFactory
            from tests.constants.common_constants import CommonConstants
            
            driver_factory_obj = DriverFactory()
            constants_obj = CommonConstants()
            driver_g = driver_factory_obj.choose_browser(
                constants_obj.get_platform())
            driver_g = driver_g.get_browser('auth_scrap')
        return driver_g

    except Exception as e:
        log_file.write_log(f"Exception occurred:{e}")
        pass

class Scraping(IScraper):
    """
    This class is responsible for dealing with web scraping and HTML content persing.
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    def scraper(self, automation_link=None) -> BeautifulSoup:
        payload = {
            "base_url": None,
            "html_content": None
        }
        user_targeted_link = self._get_user_tageted_link(automation_link)
        html_data,user_targeted_link = self._request_targeted_link(user_targeted_link)
        parser_type = "lxml"  # https://lxml.de/tutorial.html
        scraper_content = self._html_parser(html_data, parser_type)
        
        payload["base_url"] = user_targeted_link
        payload["html_content"] = scraper_content
        return payload
    
    def _auth_scrap(self) -> IAuthScraping:
        # Getting IoC Container
        choice = int(input("\n1.Auth for multipage website\n2.Auth for SPA application\n\nenter your choice: "))
        if choice == 1:
            # Creating AuthSession class instance
            auth_session_obj: IAuthScraping = AuthSession()
            return auth_session_obj
        elif choice == 2:
            # Creating DriverLogin class instance
            auth_session_obj: IAuthScraping = DriverLogin()
            return auth_session_obj

    def _get_user_tageted_link(self, automation_link=None) -> str:
        user_targeted_link = automation_link
        if automation_link is None:
            Scraping.only_for_first_link = 0
            user_targeted_link = input(
                "Please, Provide the targeted link and press ENTER: ")
        user_targeted_link = self._link_validator(user_targeted_link)
        return user_targeted_link

    def _request_targeted_link(self, targeted_link: str) -> str:
        driver = getDriver()
        return_packet: any
        if driver is not None:
                if Scraping.only_for_first_link == 0:
                        auth_required = input(
                            "*==> Is this URL required authorization for routing? If yes input 'y' and If no input 'n' and press Enter: ")
                        if auth_required.lower().replace(" ", "") == 'y':   
                            auth_scrap_obj = self._auth_scrap()
                            if auth_scrap_obj is not None:
                                driver,targeted_link = auth_scrap_obj.get_authenticated_driver(
                                    targeted_link, Constants.AUTH_CREDENTIALS, driver)
                            
                            driver.implicitly_wait(10)
                            Scraping.only_for_first_link+=1

                        elif  auth_required.lower().replace(" ", "") == 'n': 
                             Scraping.only_for_first_link+=1  

                
                driver.get(targeted_link)
                time.sleep(2)
                return_packet = driver.page_source
                # driver.close()
                return return_packet,targeted_link
        else:
            print(colored("No driver found...Please generate POM first", 'red'))
            id = ObjMapper.OBJ_MAP['robo_manager']
            route = ObjMapper.id2obj(id)
            route.menu()
            return None

    def _html_parser(self, response_content, parser: str) -> BeautifulSoup:
        html_content = BeautifulSoup(response_content, parser)
        return html_content

