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
    title="Guardar archivo",
    defaultextension=".pkl",
    filetypes=[("Pickle files", "*.pkl"), ("Joblib files", "*.joblib")]
    )

    # Si el usuario no selecciona ninguna ruta (presiona cancelar), no hace nada
    if not file_path:
        return

    # Guardar el archivo según la extensión seleccionada
    try:
        if file_path.endswith(".pkl"):
            with open(file_path, "wb") as f:
                pickle.dump(data, f)
            messagebox.showinfo("Éxito", "Archivo guardado como .pkl correctamente.")

        elif file_path.endswith(".joblib"):
            joblib.dump(data, file_path)
            messagebox.showinfo("Éxito", "Archivo guardado como .joblib correctamente.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")


def open_pkl(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

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
    data = None  # Inicializamos df con None por defecto

    try: 
        data = open_model(file_path)

    except FileNotFoundError as e:
        messagebox.showerror("Error", f"No se pudo encontrar el archivo: {str(e)}")

    except AssertionError as e:
        messagebox.showerror("Error", f"Formato inválido: {str(e)}")
    
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

    return data  # Será None si ha habido algún error y un DataFrame si se ha leido correctamente
