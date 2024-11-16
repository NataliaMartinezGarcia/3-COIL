import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import os

class FileFormatError(Exception):
    """Excepción para formatos de archivo no válidos."""
    pass

class EmptyDataError(Exception):
    """Excepción para archivos vacíos o tablas inexistentes."""
    pass

# Función común para comprobar si los distintos tipos de archivos están vacíos
def check_dataframe_empty(df, source): 
    """Verifica si un DataFrame está vacío. 
    
    Si lo está, lanza una excepción. 
    Si no lo está, devuelve el DataFrame.
    """
    if df.empty:
        raise EmptyDataError(f"The {source} does not contain data.")
    return df

def open_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except pd.errors.EmptyDataError:  # Forma de comprobar que está vacío para CSV
        raise EmptyDataError("The CSV file does not contain data.")

def open_excel(file_path):
    df = pd.read_excel(file_path)
    return check_dataframe_empty(df, "Excel file")

def open_sql(file_path):
    conn = sqlite3.connect(file_path)  # Crea una conexión con la base de datos
    cur = conn.cursor()  # Crea un cursor para ejecutar sentencias SQL
    res = cur.execute("SELECT name FROM sqlite_master")
    
    try:
        # Comprueba que exista una tabla antes de acceder a ella
        result = res.fetchone()
        if result is None: # Si no existe lanza excepción
            raise EmptyDataError("The database does not contain any tables.")
        
        table_name = result[0] # Accede a la tabla (asume que solo hay 1)
        # Carga la tabla en un DataFrame
        engine = create_engine('sqlite:///' + str(file_path))  # Crea un objeto engine
        df = pd.read_sql_table(table_name, engine)  # Carga la tabla a un DataFrame
        engine.dispose()
        return check_dataframe_empty(df, "database table")
    finally:
        conn.close()  # Termina la conexión

def open_file(file_path):
    # Comprobar si el archivo existe primero
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
    EXTENSIONS = ('.csv', '.xlsx', '.xls', '.db', '.sqlite')  # Posibles extensiones
    EXTENSION_MAP = {'.csv': open_csv, '.xlsx': open_excel, '.xls': open_excel,
                     '.db': open_sql, '.sqlite': open_sql}
    
    _, extension = os.path.splitext(file_path)  # Extrae la extensión

    # Comprueba que nos pasan archivo válido
    if extension not in EXTENSIONS:
        raise FileFormatError("Invalid file format. (Valid: .csv, .xlsx, .xls, .db, .sqlite).")
    
    # Extrae el dataframe con la función correspondiente
    return EXTENSION_MAP[extension](file_path)