"""
https://peps.python.org/pep-0591/#id2 [for future scope]

© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
from abc import ABC, abstractmethod

class IDriver(ABC):
    
    driver = ""

    @abstractmethod
    def get_browser(self, mode = None):
        """This method will install and open / run the 
        Web Driver and return the object id. The parameter 
        'mode' is by default set as None/Null. If no argument 
        is passed WebDriver will act in regular mode. Or else it
        will act according to the defined mode specified by the argument.
        Example: Headless, Disable GPU etc. 
        © BRAIN STATION 23"""
        pass
    
    