import pytest
import pandas as pd
from nan_handler import NaNHandler, ConstantValueError

@pytest.fixture
def sample_dataframe():
    """
    Fixture to provide a sample DataFrame for testing.
    This fixture creates a DataFrame with several columns and introduces NaN values 
    in various rows and columns to simulate real-world missing data scenarios.
    """
    data = {
        "A": [1, 2, None, 4],
        "B": [None, 1, 2, 3],
        "C": [1, None, None, 4],
        "D": [5, 6, 7, None],
        "E": [7, 5, 7, 8], 
        "F": [1, -2, 3, 5]
    }
    return pd.DataFrame(data)

@pytest.fixture
def nan_handler_instance(sample_dataframe):
    """
    Fixture to create an instance of NaNHandler.
    This fixture initializes the NaNHandler with the sample dataframe and specifies
    the columns to be considered for NaN handling in tests.
    """
    selected_columns = ["A", "B", "C"]
    return NaNHandler(sample_dataframe, selected_columns)

# -------------------------------------------------
# Tests for check_for_nan
# -------------------------------------------------

def test_check_for_nan_true(nan_handler_instance):
    """
    Test the check_for_nan method when NaNs are present in the selected columns.
    The method should return True and provide an accurate message about the number of NaNs in each column.
    """    
    has_nan, message = nan_handler_instance.check_for_nan()
    assert has_nan is True, "It should return True if there are NaNs in the selected columns."
    
    columns_with_nan = {"A": 1, "B": 1, "C": 2}
    for column, nan_count in columns_with_nan.items():
        assert f"- {column}: {nan_count} missing values" in message, (
            f"The message should include column {column} with {nan_count} missing values."
        )

def test_check_for_nan_false(sample_dataframe):
    """
    Test the check_for_nan method when no NaNs are present in the selected columns.
    This test checks that the method returns False and provides an appropriate message when no NaNs are found.
    """
    handler = NaNHandler(sample_dataframe, ["E", "F"])
    has_nan, message = handler.check_for_nan()
    assert not has_nan
    assert "No non-existent values were detected." in message

# Question 1: Would it be necessary to check for columns with NaN among the selected and others not?
# Question 2: Should we check for the case of no NaN in the dataframe?

# -------------------------------------------------
# Tests for preprocess
# -------------------------------------------------

# pytest.mark.parametrize: it tests each method
@pytest.mark.parametrize("method", ["Delete Rows", "Fill with Mean", "Fill with Median", "Fill with a Constant Value"])
def test_preprocess_unmodified_original(nan_handler_instance, method):
    """
    Test to ensure that the original DataFrame is not modified after preprocessing.
    After applying a preprocessing method, the original DataFrame should remain unchanged.
    """    
    df_original = nan_handler_instance._df.copy()
    nan_handler_instance.preprocess(method, constant_value=10 if method == "Fill with a Constant Value" else None)
    # Compares the original df (nan_handler_instance._df) with the copy made before preprocessing
    pd.testing.assert_frame_equal(df_original, nan_handler_instance._df)  

@pytest.mark.parametrize("method", ["Delete Rows", "Fill with Mean", "Fill with Median", "Fill with a Constant Value"])
def test_preprocess_only_selected_columns(nan_handler_instance, method):
    """
    Test that preprocessing affects only the selected columns.
    After preprocessing, only the columns selected for processing should be present in the returned DataFrame.
    """    
    processed_df = nan_handler_instance.preprocess(method, constant_value=10 if method == "Fill with a Constant Value" else None)
    assert list(processed_df.columns) == nan_handler_instance._selected_columns

def test_preprocess_delete_rows_with_nan(nan_handler_instance):
    """
    Test the 'Delete Rows' preprocessing method.
    It should remove rows containing NaN values in the selected columns.
    Check if the number of remaining rows is correct and that no NaN values remain.
    """  
    processed_df = nan_handler_instance.preprocess("Delete Rows")
    assert len(processed_df) == 1  # Only rows without NaNs should remain
    assert processed_df.isnull().sum().sum() == 0, "Rows with NaNs were not correctly deleted."

def test_preprocess_fill_mean(nan_handler_instance):
    """
    Test the 'Fill with Mean' preprocessing method.
    It should replace NaN values in the selected columns with the mean of each column.
    """    
    # Calculate the mean of the selected columns before processing
    original_means = nan_handler_instance._df[nan_handler_instance._selected_columns].mean()
    
    # Apply the "Fill with Mean" method
    processed_df = nan_handler_instance.preprocess("Fill with Mean")
    
    # Verify that there are no NaNs left in the selected columns
    assert processed_df.isnull().sum().sum() == 0, "NaNs were not replaced."
    
    # Verify that the columns with NaNs were filled with their corresponding mean
    for column in nan_handler_instance._selected_columns:
        original_column = nan_handler_instance._df[column]
        processed_column = processed_df[column]
        
        # For the rows that were originally NaN, verify they were filled with the mean
        nan_indices = original_column[original_column.isnull()].index
        for index in nan_indices:
            assert processed_column[index] == pytest.approx(original_means[column]), (
                f"The value in row {index} of column {column} was not filled with the mean."
            )

def test_preprocess_fill_median(nan_handler_instance):
    """
    Test the 'Fill with Median' preprocessing method.
    It should replace NaN values in the selected columns with the median of each column.
    """    
    # Calculate the median of the selected columns before processing
    original_medians = nan_handler_instance._df[nan_handler_instance._selected_columns].median()
    
    # Apply the "Fill with Median" method
    processed_df = nan_handler_instance.preprocess("Fill with Median")
    
    # Verify that there are no NaNs left in the selected columns
    assert processed_df.isnull().sum().sum() == 0, "NaNs were not replaced."
    
    # Verify that the columns with NaNs were filled with their corresponding median
    for column in nan_handler_instance._selected_columns:
        original_column = nan_handler_instance._df[column]
        processed_column = processed_df[column]
        
        # For the rows that were originally NaN, verify they were filled with the median
        nan_indices = original_column[original_column.isnull()].index
        for index in nan_indices:
            assert processed_column[index] == pytest.approx(original_medians[column]), (
                f"The value in row {index} of column {column} was not filled with the median."
            )

@pytest.mark.parametrize("constant_value", [0, -10, 3.14])
def test_preprocess_fill_constant(nan_handler_instance, constant_value):
    """
    Test the 'Fill with a Constant Value' preprocessing method.
    It should replace NaN values in the selected columns with a specified constant value.
    """    
    # Apply the "Fill with Constant Value" method
    processed_df = nan_handler_instance.preprocess("Fill with a Constant Value", constant_value=constant_value)
    
    # Verify that there are no NaNs left in the processed DataFrame
    assert processed_df.isnull().sum().sum() == 0, "NaNs were not replaced with the constant value."
    
    # Verify that the cells that were originally NaN now have the constant value
    for column in nan_handler_instance._selected_columns:
        original_column = nan_handler_instance._df[column]
        processed_column = processed_df[column]
        
        # For the rows where there was originally NaN, verify they were replaced with the constant value
        nan_indices = original_column[original_column.isnull()].index
        for index in nan_indices:
            assert processed_column[index] == constant_value, (
                f"The value in row {index} of column {column} was not filled with the constant value {constant_value}."
            )

def test_preprocess_fill_constant_no_value(nan_handler_instance):
    """
    Test the 'Fill with a Constant Value' method when no constant value is provided.
    It should raise a ConstantValueError if the constant value is missing.
    """    
    with pytest.raises(ConstantValueError):
        nan_handler_instance.preprocess("Fill with a Constant Value")

def test_preprocess_no_nan(nan_handler_instance):
    """
    Test preprocessing when there are no NaN values.
    The method should return a DataFrame with the selected columns without changes.
    """
    nan_handler_instance._df.fillna(0, inplace=True)
    processed_df = nan_handler_instance.preprocess("Fill with Mean")
    pd.testing.assert_frame_equal(processed_df, 
                                  nan_handler_instance._df[nan_handler_instance._selected_columns])
