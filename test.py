import flask
import pandas as pd
import sqlite3
import xml.etree.ElementTree as ET

print("Flask:", flask.__version__)
print("Pandas:", pd.__version__)
print("SQLite3 module ready:", sqlite3.sqlite_version)
print("ElementTree ready:", ET.VERSION if hasattr(ET, "VERSION") else "stdlib built-in")