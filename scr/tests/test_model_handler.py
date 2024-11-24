import pytest
import pandas as pd
import os
import pickle
import joblib
from linear_regression import LinearRegression
from model_handler import save_model, open_model, open_pkl, open_joblib

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
    
    with pytest.raises(AssertionError):
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