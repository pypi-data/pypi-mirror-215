"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from tests.drivercontroller.drivers.abstract.driver import IDriver

class Chromium(IDriver):
    
    def get_browser(self, mode = None) -> IDriver:
        self.driver = webdriver.Chrome(service=Service(\
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
        return self.driver