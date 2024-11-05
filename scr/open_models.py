import pandas as pd
import joblib 
import pickle
import sqlite3
from sqlalchemy import create_engine
import os
from tkinter import messagebox

def open_pkl(file_path):
    return pd.read_pickle(file_path) # Devuelve un dataframe


def open_joblib(file_path):
    return joblib.load(file_path)  # Cambiado para usar joblib directamente



def open_model(file_path):
    # Comprobar si el archivo existe primero
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo '{file_path}' no existe.")
    
    EXTENSIONS = ('.pkl', '.joblib') # Posibles extensiones
    # Dependiendo de la extensión le asocia una función
    EXTENSION_MAP = {'.pkl': open_pkl, '.joblib': open_joblib}
    
    _, extension = os.path.splitext(file_path) # Extrae la extensión (incluye el punto)

    # Comprueba que nos pasan archivo válido
    assert extension in EXTENSIONS, "Formato de archivo inválido. (Válidos: .pkl, .joblib)."
    # Extrae el dataframe con la función que corresponda
    return EXTENSION_MAP[extension](file_path)


def open_models_interface(file_path):
    df = None  # Inicializamos df con None por defecto

    try: 
        df = open_model(file_path)

    except FileNotFoundError as e:
        messagebox.showerror("Error", f"No se pudo encontrar el archivo: {str(e)}")

    except AssertionError as e:
        messagebox.showerror("Error", f"Formato inválido: {str(e)}")
    
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")
            
    else: # Aunque se haya leido correctamente, tenemos que comprobar si el dataframe tiene datos
        if df.empty:
            messagebox.showwarning("Advertencia", "El archivo no contiene datos. La tabla no existe.")
            df = None

    return df  # Será None si ha habido algún error y un DataFrame si se ha leido correctamente