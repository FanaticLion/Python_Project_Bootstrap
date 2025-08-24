import sqlite3
import os
from src.config import BASE_DIR

DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "app.db")

def get_connection():
    return sqlite3.connect(DB_PATH)
