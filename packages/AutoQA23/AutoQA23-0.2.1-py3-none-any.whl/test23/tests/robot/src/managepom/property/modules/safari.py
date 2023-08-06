"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
# selenium 4
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# coding: utf-8
# Ref: https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari
from selenium.webdriver.common.by import By

from tests.drivercontroller.drivers.abstract.driver import IDriver

class Safari(IDriver):
    
    def get_browser(self, mode = None)  -> IDriver:
        self.driver = webdriver.Safari()
        return self.driver