import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from nan_handler import NaNHandler, ConstantValueError
from linear_regression_interface import LinearRegressionInterface


class ColumnMenu:
    """
    A graphical interface for selecting input and output columns from a DataFrame.
    This class provides a GUI that allows users to select one input column (feature)
    and one output column (target) from a DataFrame using Tkinter widgets. It includes
    scrollable listboxes for both feature and target selection, along with a confirmation
    button to validate the selection.
    """

    def __init__(self, frame: tk.Frame, columns: list, manager: 'MenuManager'):
        """
        Initialize the column selection interface.

        Parameters:
            - frame: Parent frame where widgets will be placed
            - columns: List of available column names
            - manager: Reference to the MenuManager controller
        """

        self._frame = frame
        self._columns = columns
        self._manager = manager
        self._selected_feature = []
        self._selected_target = []

        self._init_ui()

    def _init_ui(self):
        """Initialize all UI components."""
        # Create the UI elements for feature and target selection
        self.create_features_selector()
        self.create_target_selector()
        self.create_confirm_button()

    @property
    def selected_features(self) -> list:
        """
        Get the list of selected feature column
.
        Returns:
            - list: Names of selected feature column
        """
        return self._selected_feature

    @property
    def selected_target(self) -> list:
        """
        Get the list of selected target column.

        Returns:
            - list: Names of selected taget column
        """
        return self._selected_target

    def _add_scrollbar_to_listbox(self, listbox: tk.Listbox, container: tk.Frame):
        """
        Add a scrollbar to a listbox and configure their interaction.

        Parameters:
            - listbox: Listbox widget to add scrollbar to
            - container: Frame containing the listbox
        """
        # Create scrollbar and link it with listbox
        scrollbar = tk.Scrollbar(
            container,
            orient="vertical",
            command=listbox.yview
        )
        scrollbar.pack(side="right", fill="y")
        # Configure listbox to use scrollbar
        listbox.config(yscrollcommand=scrollbar.set)

    def create_features_selector(self):
        """
        Create the feature columns selector.
        Creates a frame containing a label, a single-selection listbox, and a scrollbar
        for selecting input features. The listbox is bound to the manager's selection
        handler.
        """

        # Create frame for feature selection on the left side
        features_frame = self._create_selector_frame(
            relx=0.03,
            title="Select an input column (feature):"
        )

        # Create listbox container and components
        container = self._create_listbox_container(features_frame)
        self._feature_listbox = self._create_listbox(container)
        self._populate_listbox(self._feature_listbox)
        self._add_scrollbar_to_listbox(self._feature_listbox, container)

    def create_target_selector(self):
        """
        Create the target column selector.

        Creates a frame containing a label, a single-selection listbox, and a scrollbar
        for selecting the target variable. The listbox is bound to the manager's
        selection handler.
        """

        # Create frame for target selection on the right side
        target_frame = self._create_selector_frame(
            relx=0.97,
            title="Select an output column (target):"
        )

        container = self._create_listbox_container(target_frame)
        self._target_listbox = self._create_listbox(container)
        self._populate_listbox(self._target_listbox)
        self._add_scrollbar_to_listbox(self._target_listbox, container)

    def _create_selector_frame(self, relx: float, title: str) -> tk.Frame:
        """
        Create a frame with title for column selection.

        Parameters:
            - relx: Relative x position (0-1) for frame placement
            - title: Text to display as frame title

        Returns:
            - tk.Frame: Configured frame for selection components
        """
        # Create main frame with fixed dimensions
        frame = tk.Frame(
            self._frame,
            width=290,
            height=170,
            bg='#d0d7f2'
        )
        # Position frame using relative coordinates
        frame.place(relx=relx, rely=0.25, relwidth=0.5,
                    anchor="w" if relx < 0.5 else "e")
        # Create and position title label
        label = tk.Label(
            frame,
            text=title,
            fg='#4d598a',
            bg='#d0d7f2',
            font=("DejaVu Sans Mono", 10, 'bold'),
            width=35
        )
        label.place(relx=0.5, rely=0.1, anchor="center")

        return frame

    def _create_listbox_container(self, parent: tk.Frame) -> tk.Frame:
        """
        Create container frame for listbox and scrollbar.

        Parameters:
            - parent: Parent frame to contain the listbox

        Returns:
            - tk.Frame: Container frame for listbox components
        """
        # Create and position container frame
        container = tk.Frame(parent)
        container.place(
            relx=0.5,
            rely=0.5,
            relwidth=0.75,
            relheight=0.5,
            anchor="center"
        )
        return container

    def _create_listbox(self, container: tk.Frame) -> tk.Listbox:
        """
        Create and configure a listbox for column selection.

        Parameters:
            - container: Parent frame for the listbox

        Returns:
            - tk.Listbox: Configured listbox widget
        """
        # Create listbox with single selection mode
        listbox = tk.Listbox(
            container,
            selectmode=tk.SINGLE,
            height=5,
            exportselection=False
        )
        listbox.pack(side="left", fill="both", expand=True)
        # Bind selection event to manager's handler
        listbox.bind("<<ListboxSelect>>", self._manager.on_select)
        return listbox

    def _populate_listbox(self, listbox: tk.Listbox):
        """
        Fill listbox with column names.

        Parameters:
            - listbox: Listbox widget to populate
        """
        # Add each column name to the listbox
        for column in self._columns:
            listbox.insert(tk.END, column)

    def create_confirm_button(self):
        """
        Create the confirmation button.
        Creates a button that triggers the manager's confirm_selection method when clicked.
        The button is styled with custom colors and fonts.
        """
        # Create styled confirmation button
        confirm_button = tk.Button(
            self._frame,
            text="Confirm selection",
            command=self._manager.confirm_selection,
            font=("Arial", 11, 'bold'),
            fg="#FAF8F9",
            bg='#6677B8',
            activebackground="#808ec6",
            activeforeground="#FAF8F9",
            cursor="hand2"
        )
        # Center button in frame
        confirm_button.place(relx=0.5, rely=0.45, anchor='center')

    def get_selected_columns(self):
        """
        Store the currently selected columns from both listboxes.

        Updates the internal _selected_features and _selected_target lists with
        the current selections from the respective listboxes.

        Returns:
            - None: Updates internal selected columns lists
        """
        # Get selected features from listbox
        self._selected_feature = [
            self._feature_listbox.get(i)
            for i in self._feature_listbox.curselection()
        ]
        # Get selected target from listbox
        self._selected_target = [
            self._target_listbox.get(i)
            for i in self._target_listbox.curselection()
        ]


class MethodMenu:
    """
    A menu for selecting and applying methods to handle NaN values in data.

    This class provides a GUI interface for selecting different methods to handle
    missing values in the dataset. It includes a dropdown menu for method selection
    and additional inputs for specific methods like constant value filling.
    """
    # Available methods for handling NaN values
    METHODS = (
        "Delete Rows",
        "Fill with Mean",
        "Fill with Median",
        "Fill with a Constant Value"
    )

    def __init__(self, frame: tk.Frame, manager: 'MenuManager'):
        """
        Initialize method selection menu.

        Parameters:
            - frame: Parent frame for the menu
            - manager: Reference to MenuManager controller
        """
        self._frame = frame
        self._manager = manager
        self._method_var = tk.StringVar()  # Variable to store selected method

        self._init_ui()

    def _init_ui(self):
        """Initialize all UI components."""
        self.create_nan_selector()
        self._apply_button = self.create_apply_button()

    @property
    def method_var(self) -> tk.StringVar:
        """
        Get the variable containing selected method.

        Returns:
            - tk.StringVar: Variable containing selected method
        """
        return self._method_var

    @property
    def constant_value_input(self) -> str:
        """
        Get the value entered in constant input field.

        Returns:
            - str: Current value in constant input field
        """
        return self._constant_value_input.get()

    def create_nan_selector(self):
        """
        Create the NaN handling method selector.

        Creates a combobox for method selection and additional widgets for
        constant value input when needed. Includes appropriate labels and
        styling.
        """
        # Create all UI components for method selection
        self._create_method_label()
        self._create_method_dropdown()
        self._create_constant_input()
        self._create_separator()

    def _create_method_label(self):
        """Create label for method selector."""
        # Create and position method selection label
        label = tk.Label(
            self._frame,
            text="Select a method to handle NaN:",
            fg='#4d598a',
            bg='#d0d7f2',
            font=("DejaVu Sans Mono", 10, 'bold')
        )
        label.place(relx=0.5, rely=0.59, anchor="center")

    def _create_method_dropdown(self):
        """Create dropdown for method selection."""
        # Create combobox with predefined methods
        self._method_dropdown = ttk.Combobox(
            self._frame,
            textvariable=self._method_var,
            state="disabled",  # Initially disabled
            width=30,
            values=self.METHODS
        )
        self._method_dropdown.place(
            relx=0.5,
            rely=0.67,
            relwidth=0.5,
            anchor="center"
        )
        # Bind selection event to input toggle
        self._method_dropdown.bind(
            "<<ComboboxSelected>>",
            self.toggle_cte_input
        )

    def _create_constant_input(self):
        """Create input field for constant value."""
        # Create label and entry for constant value input
        self._constant_label = tk.Label(
            self._frame,
            text="Introduce the constant:",
            fg='#4d598a',
            bg='#d0d7f2'
        )
        self._constant_value_input = tk.Entry(
            self._frame,
            width=10,
            state="disabled"
        )

        # Hide both widgets initially
        self._constant_value_input.place_forget()
        self._constant_label.place_forget()

    def _create_separator(self):
        """Create visual separator."""
        # Create horizontal line separator
        separator = tk.Frame(self._frame, bg='#6677B8', height=3)
        separator.pack(fill=tk.X, side='bottom')

    def toggle_cte_input(self, event):
        """
        Toggle constant value input field based on method selection.

        Parameters:
            - event: Event from combobox selection
        """
        # Disable regression button when method changes
        self._manager.disable_regression_button()
        selected_method = self._method_var.get()

        # Show/hide constant input based on method
        if selected_method == "Fill with a Constant Value":
            self._show_constant_input()
        else:
            self._hide_constant_input()

        # Enable apply button if method is selected
        self._apply_button.config(
            state="normal" if selected_method else "disabled"
        )

    def _show_constant_input(self):
        """Show and enable constant value input."""
        # Position and show constant value components
        self._constant_label.place(relx=0.45, rely=0.73, anchor="center")
        self._constant_value_input.place(relx=0.6, rely=0.73, anchor="center")
        # Enable input and bind key events
        self._constant_value_input.config(state="normal")
        self._constant_value_input.bind(
            "<KeyRelease>",
            lambda event: self._manager.disable_regression_button()
        )

    def _hide_constant_input(self):
        """Hide and clear constant value input."""
        # Hide input components
        self._constant_label.place_forget()
        self._constant_value_input.place_forget()
        # Clear and disable input field
        self._constant_value_input.delete(0, "end")
        self._constant_value_input.config(state="disabled")

    def create_apply_button(self) -> tk.Button:
        """
        Create button to apply NaN handling method.

        Returns:
            - tk.Button: Configured apply button
        """
        # Create and position apply button
        apply_button = tk.Button(
            self._frame,
            text="Apply",
            command=self._manager.apply_nan_handling,
            state="disabled",
            font=("Arial", 10, 'bold'),
            fg="#FAF8F9",
            bg='#6677B8',
            activebackground="#808ec6",
            activeforeground="#FAF8F9",
            cursor="hand2"
        )
        apply_button.place(relx=0.5, rely=0.80, anchor="center")
        return apply_button

    def enable_selector(self):
        """Enable method selection dropdown."""
        # Set dropdown to readonly state (can select but not edit)
        self._method_dropdown["state"] = "readonly"

    def disable_selector(self):
        """Disable and clear method selection."""
        # Clear selection and disable dropdown
        self._method_var.set("")
        self._method_dropdown["state"] = "disabled"


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
