import pytest
import pandas as pd
import sqlite3
import os
from open_files import open_file, FileFormatError, EmptyDataError

@pytest.fixture
def setup_temp_files(tmp_path):
    """
    Crea archivos temporales para pruebas, incluyendo casos de Excel, CSV y SQLite.
    """
    # Archivo CSV válido
    csv_path = tmp_path / "valid.csv"
    csv_path.write_text("col1,col2\n1,2\n3,4")

    # Archivo CSV vacío
    empty_csv_path = tmp_path / "empty.csv"
    empty_csv_path.write_text("")

    # Archivo Excel válido
    excel_path = tmp_path / "valid.xlsx"
    pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}).to_excel(excel_path, index=False)

    # Archivo Excel vacío
    empty_excel_path = tmp_path / "empty.xlsx"
    pd.DataFrame().to_excel(empty_excel_path, index=False)

    # Archivo Excel con más de una hoja
    multi_sheet_excel_path = tmp_path / "multi_sheet.xlsx"
    with pd.ExcelWriter(multi_sheet_excel_path) as writer:
        pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}).to_excel(writer, sheet_name="Sheet1", index=False)
        pd.DataFrame({"colA": [10, 20], "colB": [30, 40]}).to_excel(writer, sheet_name="Sheet2", index=False)

    # Base de datos SQLite válida con una tabla
    db_path = tmp_path / "valid.db"
    conn = sqlite3.connect(db_path)
    pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}).to_sql("test_table", conn, index=False, if_exists="replace")
    conn.close()

    # Base de datos SQLite sin tablas
    empty_db_path = tmp_path / "empty.db"
    sqlite3.connect(empty_db_path).close()

    # Base de datos SQLite con una tabla vacía
    empty_table_db_path = tmp_path / "empty_table.db"
    conn = sqlite3.connect(empty_table_db_path)
    conn.execute("CREATE TABLE test_table (col1 INTEGER, col2 INTEGER);")
    conn.close()

    # Base de datos SQLite con más de una tabla
    multi_table_db_path = tmp_path / "multi_table.db"
    conn = sqlite3.connect(multi_table_db_path)
    pd.DataFrame({"col1": [1, 2]}).to_sql("table1", conn, index=False, if_exists="replace")
    pd.DataFrame({"colA": [10, 20]}).to_sql("table2", conn, index=False, if_exists="replace")
    conn.close()

    # Archivo inexistente
    non_existent_path = tmp_path / "non_existent.csv"

    # Archivo con formato incorrecto que sí existe
    invalid_file_path = tmp_path / "invalid.txt"
    invalid_file_path.write_text("This is a text file.")

    return {
        "csv": csv_path,
        "empty_csv": empty_csv_path,
        "excel": excel_path,
        "empty_excel": empty_excel_path,
        "multi_sheet_excel": multi_sheet_excel_path,
        "db": db_path,
        "empty_db": empty_db_path,
        "empty_table_db": empty_table_db_path,
        "multi_table_db": multi_table_db_path,
        "non_existent": non_existent_path,
        "invalid_file": invalid_file_path
    }

def test_open_file_valid_excel(setup_temp_files):
    df = open_file(setup_temp_files["excel"])
    assert not df.empty
    assert list(df.columns) == ["col1", "col2"]

def test_open_file_empty_excel(setup_temp_files):
    with pytest.raises(EmptyDataError, match="The Excel file does not contain data."):
        open_file(setup_temp_files["empty_excel"])

def test_open_file_multi_sheet_excel(setup_temp_files):
    df = open_file(setup_temp_files["multi_sheet_excel"])
    assert not df.empty
    assert list(df.columns) == ["col1", "col2"]

def test_open_file_valid_csv(setup_temp_files):
    df = open_file(setup_temp_files["csv"])
    assert not df.empty
    assert list(df.columns) == ["col1", "col2"]

def test_open_file_empty_csv(setup_temp_files):
    with pytest.raises(EmptyDataError, match="The CSV file does not contain data."):
        open_file(setup_temp_files["empty_csv"])

def test_open_file_valid_db(setup_temp_files):
    df = open_file(setup_temp_files["db"])
    assert not df.empty
    assert list(df.columns) == ["col1", "col2"]

def test_open_file_empty_db(setup_temp_files):
    with pytest.raises(EmptyDataError, match="The database does not contain any tables."):
        open_file(setup_temp_files["empty_db"])

def test_open_file_empty_table_db(setup_temp_files):
    with pytest.raises(EmptyDataError, match="The database table does not contain data."):
        open_file(setup_temp_files["empty_table_db"])

def test_open_file_multi_table_db(setup_temp_files):
    df = open_file(setup_temp_files["multi_table_db"])
    assert not df.empty
    assert list(df.columns) == ["col1"]

def test_open_file_non_existent(setup_temp_files):
    with pytest.raises(FileNotFoundError, match="The file '.*' does not exist."):
        open_file(setup_temp_files["non_existent"])

def test_open_file_invalid_extension(setup_temp_files):
    with pytest.raises(FileFormatError, match="Invalid file format."):
        open_file(setup_temp_files["invalid_file"])

def test_open_file_non_existent_invalid_extension(setup_temp_files):
    non_existent_invalid = setup_temp_files["non_existent"].with_suffix(".txt")
    with pytest.raises(FileNotFoundError, match="The file '.*' does not exist."):
        open_file(non_existent_invalid)
