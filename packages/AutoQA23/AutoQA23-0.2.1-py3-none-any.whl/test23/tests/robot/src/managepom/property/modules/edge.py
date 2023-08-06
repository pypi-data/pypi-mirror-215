"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
# selenium 4
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from tests.drivercontroller.drivers.abstract.driver import IDriver

class Edge(IDriver):
    
    def get_browser(self, mode = None)  -> IDriver:

        if mode != None:
            options = webdriver.EdgeOptions()
            # To avoid the popup.
            if mode == 'scrap':
                options.add_argument('--headless')
                options.add_experimental_option('excludeSwitches', ['enable-logging'])

            elif mode == 'optimize_scrap':
                options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
                options.add_argument('--headless')
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                options.add_argument('--disable-gpu')
            elif mode == 'auth_scrap':
                options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                options.add_argument('--headless')
                options.add_argument("start-maximized")
                options.add_argument("disable-infobars")
                options.add_argument("--disable-extensions")
                # options.add_argument("user-data-dir=#######") 
            # Ref: https://learn.microsoft.com/en-us/microsoft-edge/webdriver-chromium/?tabs=python#using-chromium-specific-options
            self.driver = webdriver.Edge(options= options,service=Service(EdgeChromiumDriverManager().install()))
            return self.driver
        else:
            self.driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
            return self.driver