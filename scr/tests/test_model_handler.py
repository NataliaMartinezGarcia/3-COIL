import pytest
import pandas as pd
import os
import pickle
import joblib
from linear_regression import LinearRegression
from model_handler import save_model, open_model, open_pkl, open_joblib
from exceptions import FileFormatError, FileNotSelectedError

@pytest.fixture
def sample_model():
    """
    Fixture to provide a sample LinearRegression model for testing.
    Creates a model with predefined values to simulate a trained model.
    """
    # Create dummy data with specific values to achieve desired test values
    x = pd.Series([1, 2, 3], name="Temperature")
    y = 10.5 + 2.3 * x  # This will give us intercept=10.5 and slope=2.3
    
    # Initialize model with required parameters
    model = LinearRegression(feature=x, target=y)
    
    # The model will automatically calculate these values during initialization
    # No need to set them manually as they are read-only properties
    return model

@pytest.fixture
def sample_model_data():
    """
    Fixture to provide sample model data dictionary.
    This represents the expected structure of saved model data.
    """
    return {
        "intercept": 10.5,
        "slope": 2.3,
        "r_squared": pytest.approx(1.0),  # Should be very close to 1 given our perfect linear data
        "mse": pytest.approx(0.0),        # Should be very close to 0 given our perfect linear data
        "feature_name": "Temperature",
        "target_name": "Sales",
        "description": "Test model"
    }

@pytest.fixture
def temp_pkl_file(tmp_path, sample_model_data):
    """
    Fixture to create a temporary pickle file containing model data.
    
    Parameters:
        tmp_path: pytest fixture providing temporary directory
        sample_model_data: fixture providing model data
    
    Returns:
        Path: path to the temporary pickle file
    """
    file_path = tmp_path / "model.pkl"
    with open(file_path, "wb") as f:
        pickle.dump(sample_model_data, f)
    return file_path

@pytest.fixture
def temp_joblib_file(tmp_path, sample_model_data):
    """
    Fixture to create a temporary joblib file containing model data.
    
    Parameters:
        tmp_path: pytest fixture providing temporary directory
        sample_model_data: fixture providing model data
    
    Returns:
        Path: path to the temporary joblib file
    """
    file_path = tmp_path / "model.joblib"
    joblib.dump(sample_model_data, file_path)
    return file_path

# -------------------------------------------------
# Tests for open_pkl and open_joblib
# -------------------------------------------------

def test_open_pkl(temp_pkl_file, sample_model_data):
    """
    Test opening a pickle file containing model data.
    Verifies that the loaded data matches the original saved data.
    """
    loaded_data = open_pkl(temp_pkl_file)
    assert loaded_data == sample_model_data
    assert loaded_data["intercept"] == pytest.approx(10.5)
    assert loaded_data["slope"] == pytest.approx(2.3)
    assert loaded_data["feature_name"] == "Temperature"

def test_open_joblib(temp_joblib_file, sample_model_data):
    """
    Test opening a joblib file containing model data.
    Verifies that the loaded data matches the original saved data.
    """
    loaded_data = open_joblib(temp_joblib_file)
    assert loaded_data == sample_model_data
    assert loaded_data["intercept"] == pytest.approx(10.5)
    assert loaded_data["slope"] == pytest.approx(2.3)
    assert loaded_data["feature_name"] == "Temperature"

# -------------------------------------------------
# Tests for open_model
# -------------------------------------------------

@pytest.mark.parametrize("file_fixture", ["temp_pkl_file", "temp_joblib_file"])
def test_open_model(file_fixture, sample_model_data, request):
    """
    Test opening model files with different formats.
    Verifies that the open_model function correctly handles both .pkl and .joblib files.
    
    Parameters:
        file_fixture: name of the fixture providing the test file
        sample_model_data: fixture providing expected model data
        request: pytest fixture for accessing other fixtures
    """
    file_path = request.getfixturevalue(file_fixture)
    loaded_data = open_model(file_path)
    assert loaded_data == sample_model_data

def test_open_model_nonexistent_file():
    """
    Test opening a non-existent file.
    Verifies that appropriate error is raised when file doesn't exist.
    """
    with pytest.raises(FileNotFoundError):
        open_model("nonexistent_file.pkl")

def test_open_model_invalid_extension(tmp_path):
    """
    Test opening a file with invalid extension.
    Verifies that appropriate error is raised for unsupported file formats.
    """
    # Create a temporary file with invalid extension
    invalid_file = tmp_path / "model.txt"
    invalid_file.touch()  # Create the file
    
    with pytest.raises(FileFormatError):
        open_model(str(invalid_file))

# -------------------------------------------------
# Tests for save_model
# -------------------------------------------------

def test_save_model_with_description(tmp_path, sample_model, monkeypatch):
    """
    Test saving a model with a description.
    Verifies that the model and its description are correctly saved.
    
    Parameters:
        tmp_path: pytest fixture providing temporary directory
        sample_model: fixture providing test model
        monkeypatch: pytest fixture for mocking
    """
    # Mock filedialog to return a specific path
    save_path = os.path.join(tmp_path, "model.pkl")
    monkeypatch.setattr('tkinter.filedialog.asksaveasfilename', 
                       lambda **kwargs: save_path)
    
    # Save model with description
    extension = save_model(sample_model, description="Test Description")
    
    # Verify the file was saved
    assert os.path.exists(save_path)
    
    # Load and verify the saved data
    with open(save_path, 'rb') as f:
        loaded_data = pickle.load(f)
    
    assert loaded_data["description"] == "Test Description"
    assert loaded_data["feature_name"] == sample_model.feature_name
    assert loaded_data["target_name"] == sample_model.target_name
    assert loaded_data["intercept"] == pytest.approx(sample_model.intercept)
    assert extension == ".pkl"

def test_save_model_cancel_save(sample_model, monkeypatch):
    """
    Test canceling the save model operation.
    Verifies that the function handles cancellation gracefully.
    
    Parameters:
        sample_model: fixture providing test model
        monkeypatch: pytest fixture for mocking
    """
    # Mock filedialog to return empty string (simulating cancel)
    monkeypatch.setattr('tkinter.filedialog.asksaveasfilename', 
                       lambda **kwargs: "")
    
    # Verify that save_model returns None when cancelled
    result = save_model(sample_model)
    assert result is None

@pytest.mark.parametrize("extension", [".pkl", ".joblib"])
def test_save_model_different_formats(tmp_path, sample_model, extension, monkeypatch):
    """
    Test saving model in different formats.
    Verifies that the model can be saved in both .pkl and .joblib formats.
    
    Parameters:
        tmp_path: pytest fixture providing temporary directory
        sample_model: fixture providing test model
        extension: file extension to test
        monkeypatch: pytest fixture for mocking
    """
    # Mock filedialog to return a specific path with the given extension
    save_path = os.path.join(tmp_path, f"model{extension}")
    monkeypatch.setattr('tkinter.filedialog.asksaveasfilename', 
                       lambda **kwargs: save_path)
    
    # Save the model
    result_extension = save_model(sample_model)
    
    # Verify the file was saved
    assert os.path.exists(save_path)
    assert result_extension == extension
    
    # Verify the saved data can be loaded
    loaded_data = open_model(save_path)
    assert loaded_data["feature_name"] == sample_model.feature_name
    assert loaded_data["target_name"] == sample_model.target_name
    assert loaded_data["intercept"] == pytest.approx(sample_model.intercept)

# -------------------------------------------------
# Tests for corrupted or invalid model files
# -------------------------------------------------

def test_open_model_corrupted_file(tmp_path):
    """
    Test opening a corrupted model file.
    Verifies that an appropriate error is raised when the file is corrupted.
    """
    # Create a corrupted file
    corrupted_file = tmp_path / "corrupted_model.pkl"
    with open(corrupted_file, "wb") as f:
        f.write(b"This is not a valid pickle or joblib file.")

    # Verify that an exception is raised
    with pytest.raises((pickle.UnpicklingError, EOFError, joblib.externals.loky.process_executor.TerminatedWorkerError)):
        open_model(str(corrupted_file))


def test_open_model_missing_keys(temp_pkl_file):
    """
    Test opening a file missing required keys.
    Verifies that an error is raised when the data is incomplete.
    """
    # Modify the contents of the pickle file to remove required keys
    incomplete_data = {"intercept": 10.5, "slope": 2.3}  # Missing other keys
    with open(temp_pkl_file, "wb") as f:
        pickle.dump(incomplete_data, f)

    # Verify that an exception is raised with a message containing the missing keys
    with pytest.raises(ValueError) as excinfo:
        open_model(temp_pkl_file)

    error_message = str(excinfo.value)

    # Validate that the error message includes all missing keys
    expected_missing_keys = {"r_squared", "mse", "feature_name", "target_name", "description"}

    # Split the error message and ensure all missing keys are reported
    assert all(key in error_message for key in expected_missing_keys), \
        f"Missing keys not reported correctly. Error message: {error_message}"
    
    # Validate that the message indicates missing keys
    assert "Missing required keys" in error_message, \
        f"Error message does not indicate missing keys. Error message: {error_message}"

def test_open_model_extra_keys(temp_pkl_file):
    """
    Test opening a file with extra keys.
    Verifies that an error is raised when the data contains unexpected keys.
    """
    # Modify the contents of the pickle file to include extra keys
    extra_data = {
        "intercept": 10.5,
        "slope": 2.3,
        "r_squared": 0.99,
        "mse": 0.01,
        "feature_name": "Temperature",
        "target_name": "Sales",
        "description": "Test model",
        "extra_key1": "unexpected_value1",
        "extra_key2": "unexpected_value2"
    }
    with open(temp_pkl_file, "wb") as f:
        pickle.dump(extra_data, f)

    # Verify that an exception is raised with the correct error message
    with pytest.raises(ValueError) as excinfo:
        open_model(temp_pkl_file)

    error_message = str(excinfo.value)

    # Define the extra keys that should appear in the error message
    unexpected_keys = {"extra_key1", "extra_key2"}

    # Validate that the error message includes all extra keys
    assert all(key in error_message for key in unexpected_keys), \
        f"Extra keys not reported correctly. Error message: {error_message}"

    # Validate that the message indicates unexpected keys
    assert "Unexpected extra keys" in error_message, \
        f"Error message does not indicate unexpected keys. Error message: {error_message}"


def test_open_model_missing_and_extra_keys(temp_pkl_file):
    """
    Test opening a file with missing and extra keys.
    Verifies that an error is raised with a detailed message for both issues.
    """
    # Modify the contents of the pickle file to contain missing and extra keys
    incorrect_data = {
        "intercept": 10.5,
        "slope": 2.3,
        "extra_key": "unexpected_value"
    }  # Missing most required keys and includes an extra key
    with open(temp_pkl_file, "wb") as f:
        pickle.dump(incorrect_data, f)

    # Verify that an exception is raised with a message containing both missing and extra keys
    with pytest.raises(ValueError) as excinfo:
        open_model(temp_pkl_file)

    error_message = str(excinfo.value)

    # Validate that the error message includes all missing and extra keys
    expected_missing_keys = {"r_squared", "mse", "feature_name", "target_name", "description"}
    expected_extra_keys = {"extra_key"}

    # Check for missing keys in the error message
    assert all(key in error_message for key in expected_missing_keys), \
        f"Missing keys not reported correctly. Error message: {error_message}"
    
    # Check for extra keys in the error message
    assert all(key in error_message for key in expected_extra_keys), \
        f"Extra keys not reported correctly. Error message: {error_message}"

    assert "Unexpected extra keys" in error_message, \
        f"Error message does not indicate unexpected keys. Error message: {error_message}"
    assert "Missing required keys" in error_message, \
        f"Error message does not indicate unexpected keys. Error message: {error_message}"
    
def test_open_model_no_file_selected():
    """
    Test that the FileNotSelectedError is raised when no file is selected.
    """
    # Simulate that the user does not select any file (empty file path)
    with pytest.raises(FileNotSelectedError, match="You haven't selected any model."):
        open_model("")
