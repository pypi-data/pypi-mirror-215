"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from tests.drivercontroller.drivers.abstract.driver import IDriver
from webdriver_manager.core.utils import ChromeType

class Brave(IDriver):
    
    def get_browser(self, mode = None) -> IDriver:
        self.driver = webdriver.Chrome(service=Service\
            (ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()))
        return self.driver