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
        raise FileNotFoundError(f"El archivo '{file_path}' no existe.")
    
    EXTENSIONS = ('.csv', '.xlsx', '.xls', '.db', '.sqlite') # Posibles extensiones
    # Dependiendo de la extensión le asocia una función
    EXTENSION_MAP = {'.csv': open_csv, '.xlsx': open_excel, '.xls': open_excel,
                     '.db': open_sql, '.sqlite': open_sql}
    
    _, extension = os.path.splitext(file_path) # Extrae la extensión (incluye el punto)

    # Comprueba que nos pasan archivo válido
    assert extension in EXTENSIONS, "Formato de archivo inválido. (Válidos: .csv, .xlsx, .xls, .db, .sqlite)."
    # Extrae el dataframe con la función que corresponda
    return EXTENSION_MAP[extension](file_path)

def main():
    # Interfaz provisional (pendiente si hay que cambiarla al hacer la interfaz gráfica)
    print("Puede importar una tabla de datos desde un archivo CSV, Excel o base de datos SQLite.")
    file_path = input("Introduzca la ruta absoluta del archivo que desea importar: ")

    try: 
        df = open_file(file_path)

    except FileNotFoundError as e:
        print("\n" + str(e))  # Mensaje de error del archivo no encontrado

    except AssertionError as e:
        print("\n" + str(e))  # Mensaje de error de formato inválido

    except IOError:
        print(f"\nEl archivo {file_path} está corrupto o hubo problemas en la lectura.")
    
    else: # Aunque se haya leido correctamente, tenemos que comprobar si el dataframe tiene datos
        if df.empty:
            print(f"\nEl archivo {file_path} está vacío. La tabla no existe.")
        else:
            print("\nArchivo leído correctamente.\n")
            print(df.head(10)) # Previsualizar las 10 primeras filas

if __name__ == "__main__":
    main()