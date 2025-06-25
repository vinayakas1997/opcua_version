from setuptools import setup ,find_packages 
from typing import List 

PROJECT_NAME = "Omron_fins_GUI"
VERSION = "0.0.1"
DESCRIPTION = "Omron FINS GUI to communicate with Omron PLCs"
AUTHOR = "VINAYAKA SAJJANSHETTY"
AUTHOR_EMAIL = "dummy@somic.inc"
REQUIREMENTS_FILE_NAME = "requirements.txt"


def get_requirements(file_path: str) -> List[str]:
    """
    This function will return a list of requirements
    """
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if '-e .' in requirements:
            requirements.remove('-e .')
    return requirements

setup(name=PROJECT_NAME,
      version=VERSION,
      description= DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
    #   url='https://www.python.org/sigs/distutils-sig/',
      packages=find_packages(),
      install_requires= get_requirements(REQUIREMENTS_FILE_NAME)
     )
