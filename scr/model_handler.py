import pandas as pd
import joblib 
import pickle
import sqlite3
from sqlalchemy import create_engine
import os
from tkinter import messagebox, filedialog, ttk  
from linear_regression import LinearRegression


def save_model(model,description = None):
   # Usar getters para acceder a los valores correctamente
    feature_name = model.feature_name
    target_name = model.target_name
    intercept = model.intercept
    slope = model.slope
    r_squared = model.r_squared
    mse = model.mse
    
    # Crear un diccionario con los datos a guardar
    data = {
        "intercept": intercept,
        "slope": slope,
        "r_squared": r_squared,
        "mse": mse,
        "feature_name": feature_name,
        "target_name": target_name,
        "description": description if description is not None else "",
    }
    
    file_path = filedialog.asksaveasfilename(
    title="Save file",
    defaultextension=".pkl",
    filetypes=[("Pickle files", "*.pkl"), ("Joblib files", "*.joblib")]
    )

    # Si el usuario no selecciona ninguna ruta (presiona cancelar), no hace nada
    if not file_path:
        return None

    # Guardar el archivo según la extensión seleccionada
    if file_path.endswith(".pkl"):
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
            return ".pkl"  # Devuelve el tipo de archivo para especificarlo en el messagebox con mensaje de éxito

    elif file_path.endswith(".joblib"):
        joblib.dump(data, file_path)
        return ".joblib"

def open_pkl(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

def open_joblib(file_path):
    return joblib.load(file_path)  # Cambiado para usar joblib directamente

def open_model(file_path):
    # Comprobar si el archivo existe primero
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
    EXTENSIONS = ('.pkl', '.joblib') # Posibles extensiones
    # Dependiendo de la extensión le asocia una función
    EXTENSION_MAP = {'.pkl': open_pkl, '.joblib': open_joblib}
    
    _, extension = os.path.splitext(file_path) # Extrae la extensión (incluye el punto)

    # Comprueba que nos pasan archivo válido
    assert extension in EXTENSIONS, "Invalid file format. (Valid: .pkl, .joblib)."

    return EXTENSION_MAP[extension](file_path)

def open_models_interface(file_path):
    data = None  # Inicializamos df con None por defecto

    try: 
        data = open_model(file_path)

    except FileNotFoundError as e:
        messagebox.showerror("Error", f"The file could not be found: {str(e)}")

    except AssertionError as e:
        messagebox.showerror("Error", f"Invalid format: {str(e)}")
    
    except Exception as e:
        messagebox.showerror("Error", f"The file could not be loaded: {str(e)}")

    return data  # Será None si ha habido algún error y un DataFrame si se ha leido correctamente
