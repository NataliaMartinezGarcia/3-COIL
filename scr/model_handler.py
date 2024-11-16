import pandas as pd
import joblib 
import pickle
import sqlite3
from sqlalchemy import create_engine
import os
from tkinter import messagebox, filedialog, ttk  
from linear_regression import LinearRegression


def save_model(model,description = None):
    """
    Save a linear regression model to a file in either pickle (.pkl) or joblib (.joblib) format.
    
    This function saves the model's parameters and metadata including feature name,
    target name, intercept, slope, R-squared value, and MSE. It prompts the user
    to choose a save location and file format through a file dialog.
    
    Args:
        model: A LinearRegression model object containing the trained model parameters
        description (str, optional): A description of the model. Defaults to None.
    
    Returns:
        str: The file extension of the saved file ('.pkl' or '.joblib'),
             or None if the save operation was cancelled.
    """
    # Use getters to access values correctly
    feature_name = model.feature_name
    target_name = model.target_name
    intercept = model.intercept
    slope = model.slope
    r_squared = model.r_squared
    mse = model.mse
    
    # Use getters to access values correctly
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

    # If user doesn't select any path (presses cancel), do nothing
    if not file_path:
        return None

    # Save the file according to the selected extension
    if file_path.endswith(".pkl"):
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
            return ".pkl"  # Returns file type to specify in success message

    elif file_path.endswith(".joblib"):
        joblib.dump(data, file_path)
        return ".joblib"

def open_pkl(file_path):
    """
    Open and load a model saved in pickle format.
    
    Args:
        file_path (str): Path to the pickle file.
    
    Returns:
        dict: The loaded model data.
    """
    with open(file_path, 'rb') as file:
        return pickle.load(file)

def open_joblib(file_path):
    """
    Open and load a model saved in joblib format.
    
    Args:
        file_path (str): Path to the joblib file.
    
    Returns:
        dict: The loaded model data.
    """
    return joblib.load(file_path) 

def open_model(file_path):
    """
    Open a saved model from either a pickle or joblib file.
    
    This function determines the appropriate method to load the model based on
    the file extension and validates the file existence and format before loading.
    
    Args:
        file_path (str): Path to the model file (.pkl or .joblib)
    
    Returns:
        dict: The loaded model data containing model parameters and metadata.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        AssertionError: If the file format is not supported (.pkl or .joblib).
    """
    # Check if file exists first
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
    EXTENSIONS = ('.pkl', '.joblib') # Possible extensions
    # Map extensions to their corresponding opening functions
    EXTENSION_MAP = {'.pkl': open_pkl, '.joblib': open_joblib}
    
    _, extension = os.path.splitext(file_path)  # Extract extension (includes the dot)

    # Verify valid file format
    assert extension in EXTENSIONS, "Invalid file format. (Valid: .pkl, .joblib)."

    return EXTENSION_MAP[extension](file_path)