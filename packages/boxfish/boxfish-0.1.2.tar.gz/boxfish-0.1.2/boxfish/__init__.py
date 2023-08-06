# __init__.py

"""Boxfish, a lightweight tool for table extraction from HTML pages."""

import pathlib

# Main modules
from boxfish.data import config, soups, website
# Main functions
from boxfish.data.config import build, create
from boxfish.data.website import extract

# Version
__version__ = (pathlib.Path(__file__).parent / "VERSION").read_text()

# Initialization
print("Initializing boxfish ...")
