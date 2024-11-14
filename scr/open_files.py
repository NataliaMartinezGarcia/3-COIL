import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import os
from tkinter import messagebox

def open_csv(file_path):
    return pd.read_csv(file_path) # Devuelve un dataframe

def open_excel(file_path):
    return pd.read_excel(file_path)

def open_sql(file_path):
    conn = sqlite3.connect(file_path) # Crea una conexión con la base de datos
    cur = conn.cursor() # Crea un cursor para ejecutar sentencias SQL
    # Devuelve una tupla con los nombres de las tablas que haya
    res = cur.execute("SELECT name FROM sqlite_master")
    
    try:
        # Consigue el nombre de la tabla (asumiendo que solo hay una, es el primer elemento)
        table_name = res.fetchone()[0]
    except: # si la tabla no existe, no hay ningún nombre 
        return pd.DataFrame() # Devuelve un dataframe vacío si no hay tabla
        # en otra función haremos una comprobacion de que, si el dataframe está vacío, la tabla no existe
    else:
        # Una vez tenemos el nombre de la tabla, la convertimos a un DataFrame
        engine = create_engine('sqlite:///' + file_path) # Crea un objeto engine
        df = pd.read_sql_table(table_name, engine) # Carga la tabla de la base de datos a un DataFrame
        engine.dispose()
        return df # devuelve el dataframe con información
    finally:  
        conn.close() # Termina la conexión

def open_file(file_path):

    # Comprobar si el archivo existe primero
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
    EXTENSIONS = ('.csv', '.xlsx', '.xls', '.db', '.sqlite') # Posibles extensiones
    # Dependiendo de la extensión le asocia una función
    EXTENSION_MAP = {'.csv': open_csv, '.xlsx': open_excel, '.xls': open_excel,
                     '.db': open_sql, '.sqlite': open_sql}
    
    _, extension = os.path.splitext(file_path) # Extrae la extensión (incluye el punto)

    # Comprueba que nos pasan archivo válido
    assert extension in EXTENSIONS, "Invalid file format. (Valid: .csv, .xlsx, .xls, .db, .sqlite)."
    # Extrae el dataframe con la función que corresponda
    return EXTENSION_MAP[extension](file_path)

def open_files_interface(file_path):
    df = None  # Inicializamos df con None por defecto

    try: 
        df = open_file(file_path)

    except FileNotFoundError as e:
        messagebox.showerror("Error", f"The file could not be found: {str(e)}")

    except AssertionError as e:
        messagebox.showerror("Error", f"Invalid format: {str(e)}")
    
    except Exception as e:
        messagebox.showerror("Error", f"The file could not be loaded: {str(e)}")
            
    else: # Aunque se haya leido correctamente, tenemos que comprobar si el dataframe tiene datos
        if df.empty:
            messagebox.showwarning("Warning", "The file does not contain data. The table does not exist.")
            df = None

    return df  # Será None si ha habido algún error y un DataFrame si se ha leido correctamente