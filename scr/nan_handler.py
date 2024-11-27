import pandas as pd


class ConstantValueError(Exception):
    """Exception raised when the constant value is not valid."""
    pass


class NaNHandler:
    """
    Class for handling the verification and management of NaN values in a DataFrame.

    This class provides methods to detect and handle missing values in specified columns
    of a pandas DataFrame using various strategies like deletion or imputation.

    Parameters:
        _df (pandas.DataFrame): The original DataFrame to process.
        _selected_columns (list): List of valid columns of the DataFrame to process.
    """

    def __init__(self, df, selected_columns):
        """
        Initialize the NaNHandler with a DataFrame and selected columns.

        Parameters:
            - df: The DataFrame to process.
            - selected_columns: List of valid column names of the DataFrame to process.
        """
        self._df = df
        self._selected_columns = list(set(selected_columns))

    def check_for_nan(self):
        """
        Verify if there are NaN values in the selected columns.

        Returns:
            - tuple: A boolean indicating if there are missing values and an informative message.
        """
        missing_info = self._df[self._selected_columns].isnull().sum()
        missing_columns = missing_info[missing_info > 0]

        if not missing_columns.empty:
            nan_message = "Non-existent values detected in the following columns:\n"
            for col, count in missing_columns.items():
                nan_message += f"- {col}: {count} missing values\n"
            return True, nan_message
        else:
            return False, "No non-existent values were detected."

    def _remove_rows(self, columns):
        """
        Remove rows with missing data from the DataFrame.

        Parameters:
           - columns (list): List of columns where rows with NaN will be removed.

        Returns:
           - pandas.DataFrame: DataFrame without rows that contained NaN in specified columns.
        """
        return self._df[columns].dropna(subset=columns).copy()

    def _fill_mean(self, columns):
        """
        Replace missing data in DataFrame columns with their mean values.

        Parameters:
            - columns (list): List of columns where NaN will be filled with mean values.

        Returns:
            - pandas.DataFrame: DataFrame with NaN values filled with column means.
        """
        return self._df[columns].fillna(self._df[columns].mean())

    def _fill_median(self, columns):
        """
        Replace missing data in DataFrame columns with their median values.

        Parameters:
            - columns (list): List of columns where NaN will be filled with median values.

        Returns:
            - pandas.DataFrame: DataFrame with NaN values filled with column medians.
        """
        return self._df[columns].fillna(self._df[columns].median())

    def _fill_constant(self, columns, constant_value):
        """
        Replace missing data in DataFrame columns with a constant value.

        Parameters:
            - columns (list): List of columns where NaN will be filled with a constant value.
            - constant_value (float): Constant value to fill NaN values with.

        Returns:
            - pandas.DataFrame: DataFrame with NaN values filled with the constant value.
        """
        return self._df[columns].fillna(constant_value)

    def preprocess(self, method, constant_value=None):
        """
        Return a preprocessed copy of the selected columns using the specified method.

        Parameters:
            - method : str
                Preprocessing method to use.
                Valid values:
                - "Delete rows"
                - "Fill with Mean"
                - "Fill with Median"
                - "Fill with a Constant Value"
            - constant_value (float, optional): Value to use when filling NaN values if method is "Fill with a Constant Value".

        Returns:
            - pandas.DataFrame: Preprocessed copy of the selected columns.

        Raises:
            - ConstantValueError: If method is "Fill with a Constant Value" and no constant value is provided.
        """
        # Methods and their corresponding functions
        METHOD_FUNCTIONS = {
            "Delete Rows": self._remove_rows,
            "Fill with Mean": self._fill_mean,
            "Fill with Median": self._fill_median,
            "Fill with a Constant Value": self._fill_constant,
        }

        # We check the method and call the corresponding function
        if method == "Fill with a Constant Value":
            if constant_value is not None:  # Check that there is a constant value
                return METHOD_FUNCTIONS[method](self._selected_columns, constant_value)
            else:  # If there is no constant value
                raise ConstantValueError(
                    "You must introduce a valid numeric value.")
        else:
            return METHOD_FUNCTIONS[method](self._selected_columns)


if __name__ == "__main__":
    # Example for using the module
    import pandas as pd

    data = {
        "Columna1": [1, 2, None, 4],
        "Columna2": [None, 1, 2, 3],
        "Columna3": [1, None, None, 4],
        "Columna4": [5, 6, 7, None],
    }
    df = pd.DataFrame(data)

    print("df Before the pre-processing")
    print(df)

    nan = NaNHandler(df, ["Columna1", "Columna2", "Columna3"])
    has_missing, message = nan.check_for_nan()
    print(message)

    new_df = nan.preprocess("Delete Rows")

    print("\nnew_df after the pre-processing")
    print(new_df)

    print("\ndf after the pre-processing")
    print(df)

    new_df = nan.preprocess("Fill with Mean")

    print("\nnew_df after the pre-processing")
    print(new_df)

    print("\ndf after the pre-processing")
    print(df)

    new_df = nan.preprocess("Fill with Median")

    print("\nnew_df after the pre-processing")
    print(new_df)

    print("\ndf after the pre-processing")
    print(df)

    new_df = nan.preprocess("Fill with a Constant Value", 0)

    print("\nnew_df after the pre-processing")
    print(new_df)

    print("\ndf after the pre-processing")
    print(df)
