import os
from setuptools import find_packages, setup

# with open('README.rst') as readme:
#     README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="messenger-business-api",
    version="1.0.0",
    author="Yuri Ramos Lima",
    author_email="yurilima93@hotmail.com",
    description="This repository is a wrapper for Meta messenger api for Messenger and Instagram",
    packages=find_packages(),
    include_package_data=True,
    # long_description=README,
    install_requires=[ "pydantic", "requests"],
    license="MIT License",
    keywords=["python","Meta", "Facebook", "Instagram", "message", "chat-bot"],
   
)
