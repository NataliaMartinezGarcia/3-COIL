import pytest
import pandas as pd
import numpy as np
from linear_regression import LinearRegression

@pytest.fixture
def sample_data():
    """
    Fixture to provide sample data for testing.
    Creates perfectly linear data to ensure predictable test results.
    """
    x = pd.Series([1, 2, 3, 4, 5], name="Temperature")
    # Create y values with known slope (2) and intercept (3)
    y = pd.Series([5, 7, 9, 11, 13], name="Sales")  # y = 2x + 3
    return x, y

@pytest.fixture
def linear_model(sample_data):
    """
    Fixture to provide a LinearRegression instance with sample data.
    """
    x, y = sample_data
    return LinearRegression(feature=x, target=y)

# -------------------------------------------------
# Tests for initialization and properties
# -------------------------------------------------

def test_initialization(sample_data):
    """
    Test proper initialization of LinearRegression class.
    Verifies that all properties are correctly set during initialization.
    """
    x, y = sample_data
    model = LinearRegression(feature=x, target=y)
    
    assert model.feature_name == "Temperature"
    assert model.target_name == "Sales"
    assert isinstance(model.predictions, np.ndarray)
    assert model.predictions is not None
    assert model.intercept is not None
    assert model.slope is not None
    assert model.r_squared is not None
    assert model.mse is not None

def test_property_access(linear_model):
    """
    Test that all properties are accessible and return expected types.
    """
    assert isinstance(linear_model.feature_name, str)
    assert isinstance(linear_model.target_name, str)
    assert isinstance(linear_model.predictions, np.ndarray)
    assert isinstance(linear_model.intercept, float)
    assert isinstance(linear_model.slope, float)
    assert isinstance(linear_model.r_squared, float)
    assert isinstance(linear_model.mse, float)

# -------------------------------------------------
# Tests for model calculations
# -------------------------------------------------

def test_perfect_linear_relationship(sample_data):
    """
    Test model performance with perfectly linear data.
    Verifies that the model correctly identifies the relationship.
    """
    x, y = sample_data
    model = LinearRegression(feature=x, target=y)
    
    # Since data is perfectly linear (y = 2x + 3)
    assert model.slope == pytest.approx(2, rel=1e-10)
    assert model.intercept == pytest.approx(3, rel=1e-10)
    assert model.r_squared == pytest.approx(1.0, rel=1e-10)
    assert model.mse == pytest.approx(0.0, rel=1e-10)

def test_predictions(linear_model, sample_data):
    """
    Test that predictions match expected values.
    """
    x, _ = sample_data
    expected_predictions = 2 * x + 3  # Based on y = 2x + 3
    
    np.testing.assert_array_almost_equal(
        linear_model.predictions,
        expected_predictions.values
    )

# -------------------------------------------------
# Tests for error handling
# -------------------------------------------------

def test_empty_data():
    """
    Test model behavior with empty data.
    """
    empty_series = pd.Series([], name="Empty")
    with pytest.raises(ValueError):
        LinearRegression(feature=empty_series, target=empty_series)

def test_mismatched_lengths():
    """
    Test error handling when feature and target have different lengths.
    """
    x = pd.Series([1, 2, 3], name="X")
    y = pd.Series([1, 2], name="Y")
    
    with pytest.raises(ValueError):
        LinearRegression(feature=x, target=y)

def test_non_numeric_data():
    """
    Test error handling with non-numeric data.
    """
    x = pd.Series(['a', 'b', 'c'], name="Letters")
    y = pd.Series([1, 2, 3], name="Numbers")
    
    with pytest.raises(TypeError):
        LinearRegression(feature=x, target=y)

# -------------------------------------------------
# Tests for different data patterns
# -------------------------------------------------

def test_constant_target():
    """
    Test model behavior when target values are constant.
    """
    x = pd.Series([1, 2, 3, 4], name="X")
    y = pd.Series([5, 5, 5, 5], name="Constant")
    
    model = LinearRegression(feature=x, target=y)
    assert model.slope == pytest.approx(0, abs=1e-10)
    assert model.r_squared == pytest.approx(0, abs=1e-10)

def test_noisy_data():
    """
    Test model behavior with noisy data.
    """
    np.random.seed(42)  # For reproducibility
    x = pd.Series(np.linspace(0, 10, 100), name="X")
    # y = 2x + 3 + noise
    noise = np.random.normal(0, 1, 100)
    y = pd.Series(2 * x + 3 + noise, name="Y")
    
    model = LinearRegression(feature=x, target=y)
    
    # With noise, we expect:
    # - slope to be approximately 2
    # - intercept to be approximately 3
    # - R² to be less than 1 but still high
    assert 1.9 < model.slope < 2.1
    assert 2.8 < model.intercept < 3.2
    assert 0.95 < model.r_squared < 1.0
    assert model.mse > 0

def test_negative_correlation():
    """
    Test model behavior with negatively correlated data.
    """
    x = pd.Series([1, 2, 3, 4, 5], name="X")
    y = pd.Series([10, 8, 6, 4, 2], name="Y")  # y = -2x + 12
    
    model = LinearRegression(feature=x, target=y)
    
    assert model.slope == pytest.approx(-2, rel=1e-10)
    assert model.intercept == pytest.approx(12, rel=1e-10)
    assert model.r_squared == pytest.approx(1.0, rel=1e-10)