import os
from abc import ABC
from tests.config import Configuration


class Constants(ABC):
    """
     This abstract class holds all the constant variables which can be 
     commonly used in this automation application. These variables are mostly
     used for managing the priority sequence.                                 
     © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    ROOT_PATH = Configuration.ROOT_BASE_PATH
    PAGE_LOCATOR_DIRECTORY_PATH = str(
        os.path.join(ROOT_PATH, "pages", "locators"))
    PAGE_DIRECTORY_PATH = str(os.path.join(ROOT_PATH, "pages"))
    NAV_BAR_FILE_PATH = str(os.path.join(
        ROOT_PATH, PAGE_LOCATOR_DIRECTORY_PATH, "nav_bar_locators.py"))
    NAV_TARGETED_HTML_TAGS = ['a', 'button', 'input']
    """For Navigation bar our application will look for these specific tags to identify pages."""
    OPTIONAL_HTML_ATTR = ['placeholder', 'title', 'value', 'alt']
    """If no inner text is found our application will look for these following attributes."""
    PRIORITY_ATTRIBUTES_AS_LOCATOR = ['id', 'name', 'type', 'title']
    """When Scraper finds a HTML tag it will look for a unique identifier as a locator. The
    elements in this list will be considered as priority according to their serial"""
    PRIORITY_ATTRIBUTE_FOR_NAVIDENTIFICATION = {
        'class': ['navbar', 'bar', 'menu', 'sticky-top', 'collapse', 'navbar-collapse'],
        'name': [],
        'role': [],
        'id': ['navbarToggler']
    }
    PRIORITY_ATTRIBUTES_IN_PAGE_BODY = ['a', 'button', 'input']
    AUTH_CREDENTIALS: dict = {
        'token_name': 'csrf',
        'token_value': '0xdEmo12345',
        'user_field_name': 'username',
        'user_field_value': 'exampleName',
        'password_field_name': 'password',
        'password_field_value': 'examplePass'
    }
    GENERAL_HTTP_HEADER: dict = {
        # If required add keys and values
    }
    SESSION_DATA: dict = {
        # AUTH_CREDENTIALS['user_field_name']: AUTH_CREDENTIALS['user_field_value'],
        # AUTH_CREDENTIALS['password_field_name']: AUTH_CREDENTIALS['password_field_value']
    }
    PRIORITY_BODY_ATTRIBUTES_WITH_IGNORE_VALUE_LIST = {
        'type': ['hidden'],
    }  # Not in use. For Future use only
