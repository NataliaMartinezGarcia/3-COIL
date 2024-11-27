import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import os


class FileFormatError(Exception):
    """Exception for invalid file formats."""
    pass


class EmptyDataError(Exception):
    """Exception for empty files or non-existent tables."""
    pass

# Common function to check if different types of files are empty


def check_dataframe_empty(df, source):
    """
    Verify if a DataFrame is empty.

    Parameters:
        - df (pandas.DataFrame): DataFrame to check.
        - source (str): Description of the data source for error messages.

    Returns:
        - pandas.DataFrame: The input DataFrame if not empty.

    Raises:
        - EmptyDataError: If the DataFrame is empty.
    """
    if df.empty:
        raise EmptyDataError(f"The {source} does not contain data.")
    return df


def open_csv(file_path):
    """
    Open and read a CSV file into a DataFrame.

    Parameters
        - file_path (str): Path to the CSV file.

    Returns:
        - pandas.DataFrame: DataFrame containing the CSV data.

    Raises:
        - EmptyDataError: If the CSV file is empty.
    """
    try:
        return pd.read_csv(file_path)
    except pd.errors.EmptyDataError:  # Check if it is empty for CSV
        raise EmptyDataError("The CSV file does not contain data.")


def open_excel(file_path):
    """
    Open and read an Excel file into a DataFrame.

    Parameters:
        - file_path (str):Path to the Excel file.

    Returns
        - pandas.DataFrame: DataFrame containing the Excel data.

    Raises:
        - EmptyDataError: If the Excel file is empty.
    """
    df = pd.read_excel(file_path)
    return check_dataframe_empty(df, "Excel file")


def open_sql(file_path):
    """Open and read a SQLite database table into a DataFrame.

    Parameters:
        - file_path (str): Path to the SQLite database file.

    Returns:
        - pandas.DataFrame: DataFrame containing the database table data.

    Raises:
        - EmptyDataError: If the database has no tables or if the table is empty.
    """
    conn = sqlite3.connect(file_path)  # Creates a conexion with the database
    cur = conn.cursor()  # Create a cursor to execute SQL statements
    res = cur.execute("SELECT name FROM sqlite_master")

    try:
        # Checks that a table exists before accessing it
        result = res.fetchone()
        if result is None:  # If it does not exist, it throws an exception
            raise EmptyDataError("The database does not contain any tables.")

        table_name = result[0]  # Access the table (assume there is only 1)
        # Loads the table in a DataFrame
        # Create an engine object
        engine = create_engine('sqlite:///' + str(file_path))
        # Load the table into a DataFrame
        df = pd.read_sql_table(table_name, engine)
        engine.dispose()
        return check_dataframe_empty(df, "database table")
    finally:
        conn.close()  # Ends the connection


def open_file(file_path):
    """
    Open and read data from various file formats into a DataFrame.

    Supports CSV, Excel (.xlsx, .xls), and SQLite (.db, .sqlite) files.

    Parameters:
        - file_path (str):Path to the file to open.

    Returns
        - pandas.DataFrame: DataFrame containing the file data.

    Raises:
        - FileNotFoundError: If the file does not exist.
        - FileFormatError: If the file format is not supported.
        - EmptyDataError: If the file or database table is empty.
    """
    # First check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    EXTENSIONS = ('.csv', '.xlsx', '.xls', '.db',
                  '.sqlite')  # Possible extensions
    EXTENSION_MAP = {'.csv': open_csv, '.xlsx': open_excel, '.xls': open_excel,
                     '.db': open_sql, '.sqlite': open_sql}

    _, extension = os.path.splitext(file_path)  # Extract the extension

    # Check that valid file is being passed
    if extension not in EXTENSIONS:
        raise FileFormatError(
            "Invalid file format. (Valid: .csv, .xlsx, .xls, .db, .sqlite).")

    # Extract the dataframe with the corresponding function
    return EXTENSION_MAP[extension](file_path)
