import pandas as pd
import joblib
import pickle
import sqlite3
from sqlalchemy import create_engine
import os
from tkinter import messagebox, filedialog, ttk
from linear_regression import LinearRegression
from exceptions import FileNotSelectedError, FileFormatError


def save_model(model, description=None):
    """
    Save a linear regression model to a file in either pickle (.pkl) or joblib (.joblib) format.

    This function saves the model's parameters and metadata including feature name,
    target name, intercept, slope, R-squared value, and MSE. It prompts the user
    to choose a save location and file format through a file dialog.

    Parameters:
        - model: A LinearRegression model object containing the trained model parameters
        - description (str, optional): A description of the model. Defaults to None.

    Returns:
        - str: The file extension of the saved file ('.pkl' or '.joblib'),
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

    Parameters:
        - file_path (str): Path to the pickle file.

    Returns:
        - dict: The loaded model data.
    """
    with open(file_path, 'rb') as file:
        return pickle.load(file)


def open_joblib(file_path):
    """
    Open and load a model saved in joblib format.

    Parameters:
        - file_path (str): Path to the joblib file.

    Returns:
       - dict: The loaded model data.
    """
    return joblib.load(file_path)


def open_model(file_path):
    """
    Open a saved model from either a pickle or joblib file.

    Parameters:
        - file_path (str): Path to the model file (.pkl or .joblib)

    Returns:
        - dict: The loaded model data containing model parameters and metadata.

    Raises:
        - FileNotSelectedError: If the file path is empty.
        - FileNotFoundError: If the specified file does not exist.
        - AssertionError: If the file format is not supported (.pkl or .joblib).
        - ValueError: If the file contains invalid or incomplete data.
    """
    EXTENSIONS = ('.pkl', '.joblib')  # Possible extensions
    REQUIRED_KEYS = {"intercept", "slope", "r_squared", "mse", "feature_name", "target_name", "description"}

    # Map extensions to their corresponding opening functions
    EXTENSION_MAP = {'.pkl': open_pkl, '.joblib': open_joblib}

    # Extract extension (includes the dot)
    _, extension = os.path.splitext(file_path)
    
    # Check if there is a filepath
    if file_path == "":
        raise FileNotSelectedError("You haven't selected any model.")
    
    # Verify valid file format first
    if extension not in EXTENSIONS:
        raise FileFormatError("Invalid file format. (Valid: .pkl, .joblib).")

    # Then check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    # Load the data using the appropriate function
    loaded_data = EXTENSION_MAP[extension](file_path)

    # Verify the data contains all required keys
    if not isinstance(loaded_data, dict):
        raise ValueError("Invalid model data format. The data is not a dictionary.")

    # Determine the keys that are missing from the loaded data
    missing_keys = REQUIRED_KEYS - loaded_data.keys()
    # Determine the keys that are present but not expected
    extra_keys = loaded_data.keys() - REQUIRED_KEYS

    # If there are missing or extra keys, generate a detailed error message
    if missing_keys or extra_keys:
        error_message = []
        if missing_keys:
            error_message.append(f"Missing required keys: {', '.join(missing_keys)}.")
        if extra_keys:
            error_message.append(f"Unexpected extra keys: {', '.join(extra_keys)}.")
        raise ValueError(" ".join(error_message))

    return loaded_data