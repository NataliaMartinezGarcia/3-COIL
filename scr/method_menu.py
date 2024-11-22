import tkinter as tk
from tkinter import ttk

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

    def __init__(self, frame: tk.Frame, manager):
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
    
    def apply_button_disable(self):
        """Disables the button that applies the method selection."""
        self._apply_button.config(state="disabled")

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
        # self._manager.disable_regression_button()
        self._manager.on_dropdown_select(event)
        selected_method = self._method_var.get()

        # Show/hide constant input based on method
        if selected_method == "Fill with a Constant Value":
            self._show_constant_input()
        else:
            self.hide_constant_input()

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
            self._manager.on_dropdown_select
        )        

    def hide_constant_input(self):
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
