import string
import random
from num2words import num2words
from .validators import Validators


class Correctors:
    """This class is one kind of filter which holds all the correction mechanism services. © BRAIN STATION 23"""

    def code_element_name_corrector(self, element_name: str) -> str:
        """This method is able to take any string and convert it into a python 
        class/ function/ variable declarable word according to PEP-8. © BRAIN STATION 23"""
        updated_element_name: list = []
        if Validators.code_element_name_validator(self, element_name):
            return element_name
        else:
            # Number to Text converter
            if element_name[0].isdigit():
                updated_element_name = list(element_name)
                updated_element_name[0] = num2words(element_name[0])
                return "".join(updated_element_name)
            # Text Cleaner (Space remover from the front and back)
            if element_name[0] == "_" or element_name[len(element_name)-1] == "_" or element_name[0] == " " or element_name[len(element_name)-1] == " ":
                element_name.replace("_", " ")
                element_name.strip()
                return element_name
            return ''.join(random.sample((string.ascii_uppercase+string.digits), 6))
