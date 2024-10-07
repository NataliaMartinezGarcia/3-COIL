import pandas as pd
import sqlite3
from sqlalchemy import create_engine

def open_csv(file_path):
    return pd.read_csv(file_path) # Devuelve un dataframe

def open_excel(file_path):
    return pd.read_excel(file_path)

def open_sql(file_path):
    conn = sqlite3.connect(file_path) # Crea una conexión con la base de datos
    cur = conn.cursor() # Crea un cursor para ejecutar sentencias SQL
    res = cur.execute("SELECT name FROM sqlite_master")
    table_name = res.fetchone()[0] # Consigue el nombre de la tabla (asumiendo que solo hay una)
    conn.close() # Termina la conexión

    # Una vez tenemos el nombre de la tabla, la convertimos a un DataFrame
    engine = create_engine('sqlite:///' + file_path) # Crea un objeto engine
    df = pd.read_sql_table(table_name, engine) # Carga la tabla de la base de datos a un DataFrame
    engine.dispose()    
    return df