import pandas as pd
import sqlite3
from sqlalchemy import create_engine

def open_csv(file_path):
    return pd.read_csv(file_path)

def open_excel(file_path):
    return pd.read_excel(file_path)

