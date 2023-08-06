from setuptools import setup,find_packages
from typing import List
REQUIREMENT_FILE_NAME="requirements.txt"
Project_Name="PYPI PUBLISHING"
Version="0.0.0.1"
AUTHOR="Abhishek"
DESCRIPTION="Experiment For publishing"
PACKAGES=["Common_functions"]



setup(

    name=Project_Name,
    version=Version,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),
    long_description="foo bar baz"
    


)

