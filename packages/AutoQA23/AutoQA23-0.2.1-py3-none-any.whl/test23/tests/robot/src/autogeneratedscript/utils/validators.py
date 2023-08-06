class Validators:
    """This class holds all the validation functionality to serve 
    the utility services. © BRAIN STATION 23"""

    def code_element_name_validator(self, element_name: str) -> bool:
        """This method is to check only the common standards of PEP-8. © BRAIN STATION 23"""
        if element_name[0].isdigit() \
            or element_name[0] == "_" \
                or element_name[len(element_name)-1] == "_":
            return False
        else:
            return True
