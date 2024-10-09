import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import os

def open_csv(file_path):
    return pd.read_csv(file_path) # Devuelve un dataframe

def open_excel(file_path):
    return pd.read_excel(file_path)

def open_sql(file_path):
    conn = sqlite3.connect(file_path) # Crea una conexión con la base de datos
    cur = conn.cursor() # Crea un cursor para ejecutar sentencias SQL
    # Devuelve una tupla con los nombres de las tablas que haya
    res = cur.execute("SELECT name FROM sqlite_master")
    # Consigue el nombre de la tabla (asumiendo que solo hay una)
    table_name = res.fetchone()[0]
    conn.close() # Termina la conexión

    # Una vez tenemos el nombre de la tabla, la convertimos a un DataFrame
    engine = create_engine('sqlite:///' + file_path) # Crea un objeto engine
    df = pd.read_sql_table(table_name, engine) # Carga la tabla de la base de datos a un DataFrame
    engine.dispose()  
    return df

def open_file(file_path):
    # Se asume que el archivo existe!
    EXTENSIONS = ('.csv', '.xlsx', '.xls', '.db', '.sqlite') # Posibles extensiones
    # Dependiendo de la extensión le asocia una función
    EXTENSION_MAP = {'.csv': open_csv, '.xlsx': open_excel, '.xls': open_excel,
                     '.db': open_sql, '.sqlite': open_sql}
    
    _, extension = os.path.splitext(file_path) # Extrae la extensión (incluye el punto)

    # Comprueba que nos pasan archivo válido
    assert extension in EXTENSIONS, "Formato de archivo inválido"
    # Extrae el dataframe con la función que corresponda
    return EXTENSION_MAP[extension](file_path)