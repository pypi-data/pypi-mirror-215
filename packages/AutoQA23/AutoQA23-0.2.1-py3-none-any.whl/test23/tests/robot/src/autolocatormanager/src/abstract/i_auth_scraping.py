from abc import ABC, abstractmethod
from typing import Any



class IAuthScraping(ABC):
    """
    # For Authorize Crawling and Scraping in Web
    This is an abstract class which is a skeleton for login with valid credentials and
    return authenticated webdriver. After that we will reuse this webdriver for scraping.
    There are one public methods
        * get_authenticated_driver => will return the authenticated web driver

    © BRAIN STATION 23 | Design and Development: Md. Sabbir Hossain (BS1078)
    """

    @abstractmethod
    def get_authenticated_driver(self, target_link: str, auth_credentials: dict = None, driver_obj: Any = None) -> Any:
        pass