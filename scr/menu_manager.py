import tkinter as tk
from tkinter import messagebox
import pandas as pd
from nan_handler import NaNHandler, ConstantValueError
from linear_regression_interface import LinearRegressionInterface
from column_menu import ColumnMenu
from method_menu import MethodMenu

class MenuManager:
    """
    Coordinates column selection and NaN handling interfaces.

    This class manages the interaction between the column selection menu and the
    NaN handling menu, coordinates data preprocessing, and handles the creation
    of the linear regression model.
    """
    # Available methods for NaN handling
    METHOD_NAMES = (
        "Delete Rows",
        "Fill with Mean",
        "Fill with Median",
        "Fill with a Constant Value"
    )

    def __init__(
        self,
        app,
        frame: tk.Frame,
        columns: list,
        df: pd.DataFrame,
        chart_frame: tk.Frame
    ):
        """
        Initialize menu manager with necessary components.

        Parameters:
            - app: Main application instance
            - frame: Frame for menu components
            - columns: List of available column names
            - df: Input DataFrame
            - chart_frame: Frame for displaying charts
        """
        self._app = app
        self._frame = frame
        self._columns = columns
        self._df = df
        self._new_df = None  # Will store processed DataFrame
        self._chart_frame = chart_frame

        self._init_components()
        self._init_debug_print()

    def _init_components(self):
        """Initialize menu components."""
        self._column_menu = ColumnMenu(self._frame, self._columns, self)
        self._method_menu = MethodMenu(self._frame, self)
        self.create_regression_button()
        self._app.scroll_window.update()

    def _init_debug_print(self):
        """Print initial debug information."""
        # Print original and processed DataFrames
        print("df Before pre-processing")
        print(self._df)
        print("new_df Before pre-processing")
        print(self._new_df)

    @property
    def df(self) -> pd.DataFrame:
        """
        Get original DataFrame.

        Returns:
            - pd.DataFrame: Original input DataFrame
        """
        return self._df

    @property
    def new_df(self) -> pd.DataFrame:
        """
        Get processed DataFrame.

        Returns:
            - pd.DataFrame: Processed DataFrame or None if not processed
        """
        return self._new_df

    def on_select(self, event):
        """
        Handle selection events from the column listboxes.
        Disables the method selector and regression button when column selection changes.

        Parameters:
            - event: Selection change event
        """
        # Reset method selection when columns change
        self._method_menu.disable_selector()
        self.disable_regression_button()

    def create_regression_button(self):
        """
        Create the button for initiating linear regression model creation.
        Creates and places a styled button that triggers the linear regression
        model creation process. The button is initially disabled.
        """
        # Create and position regression button
        self._regression_button = tk.Button(
            self._frame,
            text="Create Linear Regression Model",
            command=self.create_linear_model,
            state="disabled",
            font=("Arial", 10, 'bold'),
            fg="#FAF8F9",
            bg='#6677B8',
            activebackground="#808ec6",
            activeforeground="#FAF8F9",
            cursor="hand2"
        )
        self._regression_button.place(relx=0.5, rely=0.93, anchor='center')

    def enable_regression_button(self):
        """Enable regression model creation."""
        self._regression_button.config(state="normal")

    def disable_regression_button(self):
        """Disable regression model creation."""
        self._regression_button.config(state="disabled")

    def confirm_selection(self):
        """
        Validate and confirm the column selection.

        Updates the selected features and target variables, checks for NaN values
        in the selected columns, and enables/disables the appropriate interface
        elements based on the presence of NaN values.

        Displays appropriate message boxes for errors and success confirmations.
        """
        # Get current selection from listboxes
        self._column_menu.get_selected_columns()

        # Validate selection and proceed if valid
        if not self._validate_selection():
            return

        self._show_success_message()
        self._handle_nan_checking()

    def _validate_selection(self) -> bool:
        """
        Check if both feature and target columns are selected.

        Returns:
            - bool: True if selection is valid, False otherwise
        """
        # Check feature selection
        if not self._column_menu.selected_features:
            messagebox.showerror(
                "Error",
                "You must select an input column (feature)."
            )
            return False

        # Check target selection
        if not self._column_menu.selected_target:
            messagebox.showerror(
                "Error",
                "You must select an output column (target)."
            )
            return False

        return True

    def _show_success_message(self):
        """Show success message with selected columns."""
        # Format column names for display
        f_cols = ', '.join(self._column_menu.selected_features)
        t_col = ', '.join(self._column_menu.selected_target)
        # Show selection confirmation
        messagebox.showinfo(
            "Success",
            f"Feature: {f_cols}\nTarget: {t_col}"
        )

    def _handle_nan_checking(self):
        """Check for NaN values and update UI accordingly."""
        # Combine selected columns
        selected_columns = (
            self._column_menu.selected_features +
            self._column_menu.selected_target
        )
        # Initialize NaN handler
        self._nan_handler = NaNHandler(
            self._df,
            self.METHOD_NAMES,
            selected_columns
        )
        # Check for missing values
        has_missing, nan_message = self._nan_handler.check_for_nan()
        messagebox.showinfo("Non-existent values", nan_message)
        # Update UI based on presence of NaN values
        if has_missing:
            self._method_menu.enable_selector()
            self.disable_regression_button()
        else:
            self._method_menu.disable_selector()
            self.enable_regression_button()

    def apply_nan_handling(self):
        """
        Apply the selected NaN handling method to the data.

        Processes the data using the selected method and constant value (if applicable).
        Handles validation of constant values and displays appropriate error messages.
        Enables the regression button if preprocessing is successful.

        Raises:
            - ValueError: If the constant value input is not a valid number.
            - ConstantValueError: If there's an error with the constant value handling.
        """
        # Get selected method and validate constant value
        method = self._method_menu.method_var.get()
        constant_value = self._validate_constant_value()
        # Check for constant value when required
        if constant_value is None and method == "Fill with a Constant Value":
            return

        try:
            # Process data with selected method
            self._new_df = self._nan_handler.preprocess(method, constant_value)
            self._show_preprocessing_success()
        except ConstantValueError as e:
            messagebox.showerror("Error", str(e))

    def _validate_constant_value(self) -> float:
        """
        Validate and convert constant value input.

         Returns:
            - float: Validated constant value or None if invalid/empty
        """
        # Get input value
        value = self._method_menu.constant_value_input
        # Check if empty
        if not value or value.strip() == "":
            return None

        try:
            # Try to convert to float
            return float(value)
        except ValueError:
            messagebox.showerror(
                "Error",
                "The constant value must be a number."
            )
            return None

    def _show_preprocessing_success(self):
        """Show success message after preprocessing."""
        # Print debug information
        print("\ndf After pre-processing")
        print(self._df)
        print("\nnew_df After pre-processing")
        print(self._new_df)
        # Show success message
        messagebox.showinfo(
            "Success",
            "Non-existent data handling has been successfully applied."
        )
        self.enable_regression_button()

    def create_linear_model(self):
        """
        Create and display the linear regression model.

        Creates a linear regression model using the selected feature and target columns.
        Validates data sufficiency and displays the regression results in the chart frame.

        Displays appropriate error messages if there are issues with the data or selection.
        """
        # Validate prerequisites
        if not self._validate_model_prerequisites():
            return
        # Use processed DataFrame if available, otherwise use original
        df_to_use = self._new_df if self._new_df is not None else self._df
        # Get selected feature and target columns
        feature = df_to_use[self._column_menu.selected_features[0]]
        target = df_to_use[self._column_menu.selected_target[0]]
        # Check data sufficiency
        if not self._validate_data_sufficiency(feature, target):
            return

        self._show_model_creation()

    def _validate_model_prerequisites(self) -> bool:
        """
        Validate that necessary columns are selected.

        Returns:
            - bool: True if prerequisites are met, False otherwise
        """
        # Check if both columns are selected
        if not self._column_menu.selected_features or not self._column_menu.selected_target:
            messagebox.showerror(
                "Error",
                "You must select input and output columns before creating the model."
            )
            return False
        return True

    def _validate_data_sufficiency(self, feature: pd.Series, target: pd.Series) -> bool:
        """
        Check if there's enough data for regression.

        Parameters:
            - feature: Feature column data
            - target: Target column data

        Returns:
            - bool: True if enough data exists, False otherwise
        """
        # Need at least 2 points for regression
        if len(feature) < 2 or len(target) < 2:
            messagebox.showerror(
                "Error",
                "There isn't enough data to create the regression model."
            )
            return False
        return True

    def _show_model_creation(self):
        """Show model creation success and create visualization."""
        # Show success message
        success = messagebox.showinfo(
            "Success",
            "The linear regression model will be created successfully.\n"
            "Press OK to see the results."
        )

        if success == 'ok':
            # Clear previous chart
            self.clear_frame(self._chart_frame)
            df_to_use = self._new_df if self._new_df is not None else self._df
            # Clear previous chart
            LinearRegressionInterface(
                self._chart_frame,
                df_to_use[self._column_menu.selected_features[0]],
                df_to_use[self._column_menu.selected_target[0]]
            )
            self._app.scroll_window.update()

    @staticmethod
    def clear_frame(frame: tk.Frame):
        """
        Remove all widgets from a frame.

        Parameters:
            - frame: Frame to clear
        """
        # Destroy all child widgets
        for widget in frame.winfo_children():
            widget.destroy()
