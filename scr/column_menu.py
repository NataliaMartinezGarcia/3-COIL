import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from nan_handler import NaNHandler, ConstantValueError
from linear_regression_interface import LinearRegressionInterface

# Class that implements the interface for selecting input and output columns
class ColumnMenu:
    """
    A graphical interface for selecting input and output columns from a DataFrame.
    
    This class provides a GUI that allows users to select one input column (feature)
    and one output column (target) from a DataFrame using Tkinter widgets. It includes
    scrollable listboxes for both feature and target selection, along with a confirmation
    button to validate the selection.
    
    Attributes:
        _frame (tk.Frame): The main frame where all widgets will be placed.
        _columns (list): List of available column names for selection.
        _manager (MenuManager): Controller object that handles selection logic and confirmation.
        _selected_features (list): List of selected feature column names.
        _selected_target (list): List containing the selected target column name.
        _feature_listbox (tk.Listbox): Listbox widget for selecting feature columns.
        _target_listbox (tk.Listbox): Listbox widget for selecting target column.
    """
    def __init__(self, frame, columns, manager):
        """
        Initialize the column selection menu.
        
        Parameters
            frame (tk.Frame): Parent frame where widgets will be placed.
            columns (list): List of column names from the DataFrame.
            manager (MenuManager): Controller object for handling selection and confirmation logic.
        """
        self._frame = frame
        self._columns = columns
        self._manager = manager
        self._selected_features = []
        self._selected_target = []

        self.create_features_selector()
        self.create_target_selector()
        self.create_confirm_button()

    @property
    def selected_features(self):
        """ 
        Get the list of selected feature columns.
        
        Returns:
            list: Names of columns selected as features.
        """
        return self._selected_features

    @property
    def selected_target(self):
        """
        Get the selected target column.
        
        Returns:
            list: List containing the name of the selected target column.
        """
        return self._selected_target

    def add_scrollbar_to_listbox(self, listbox, container_frame):
        """
        Add a vertical scrollbar to a listbox within a container frame.
        
        Parameters:
            listbox (tk.Listbox): The listbox to add the scrollbar to.
            container_frame (tk.Frame): Frame containing the listbox where the scrollbar will be placed.
        """
        
        # Create and place the vertical scrollbar
        scrollbar = tk.Scrollbar(container_frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

    def create_features_selector(self):
        """
        Create the feature columns selector.
        
        Creates a frame containing a label, a single-selection listbox, and a scrollbar
        for selecting input features. The listbox is bound to the manager's selection
        handler.
        """
        # Main frame containing the label and the container_frame with the listbox and scrollbar
        features_frame = tk.Frame(self._frame, width=290, height=170,bg = '#d0d7f2')
        features_frame.place(relx=0.03, rely=0.25, relwidth=0.5, anchor="w")

        # Label
        label = tk.Label(features_frame, text="Select an input column (feature):", fg = '#4d598a', bg = '#d0d7f2',
                                font= ("DejaVu Sans Mono",10, 'bold'),width = 35)
        label.place(relx=0.5, rely=0.1, anchor="center")
        
        # Container that holds the listbox and scrollbar together
        container_frame = tk.Frame(features_frame)
        container_frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.5, anchor="center")

        # Create the Listbox and place it on the left side of the container_frame
        self._feature_listbox = tk.Listbox(container_frame, selectmode=tk.SINGLE, height=5, exportselection=False)
        self._feature_listbox.pack(side="left", fill="both", expand=True)
        self._feature_listbox.bind("<<ListboxSelect>>", self._manager.on_select)

        for column in self._columns:
            self._feature_listbox.insert(tk.END, column)

        # Call the function to add the scrollbar to the Listbox
        self.add_scrollbar_to_listbox(self._feature_listbox, container_frame)

    def create_target_selector(self):
        """
        Create the target column selector.
        
        Creates a frame containing a label, a single-selection listbox, and a scrollbar
        for selecting the target variable. The listbox is bound to the manager's
        selection handler.
        """
        target_frame = tk.Frame(self._frame, width=280, height=170, bg = '#d0d7f2')
        target_frame.place(relx=0.97, rely=0.25, relwidth=0.5, anchor="e")

        label = tk.Label(target_frame, text="Select an output column (target):", fg = '#4d598a', bg = '#d0d7f2',
                                font= ("DejaVu Sans Mono",10, 'bold'),width = 35)
        label.place(relx=0.5, rely=0.1, anchor="center")

        # Container that holds the listbox and scrollbar together
        container_frame = tk.Frame(target_frame)
        container_frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.5, anchor="center")

        self._target_listbox = tk.Listbox(container_frame, selectmode=tk.SINGLE, height=5, exportselection=False)
        self._target_listbox.bind("<<ListboxSelect>>", self._manager.on_select)
        # We use pack so that it expands within the frame that packs it with the scrollbar
        self._target_listbox.pack(side="left", fill="both", expand=True)

        for column in self._columns:
            self._target_listbox.insert(tk.END, column)

        # Call the function to add the scrollbar to the Listbox
        self.add_scrollbar_to_listbox(self._target_listbox, container_frame)

    def create_confirm_button(self):
        """
        Create the confirmation button.
        
        Creates a button that triggers the manager's confirm_selection method when clicked.
        The button is styled with custom colors and fonts.
        """
        confirm_button = tk.Button(self._frame, text="Confirm selection", command=self._manager.confirm_selection,
                                   font=("Arial", 11,'bold'), fg="#FAF8F9", bg = '#6677B8' ,activebackground="#808ec6",
                                   activeforeground="#FAF8F9",cursor="hand2" )
        
        confirm_button.place(relx=0.5, rely=0.45, anchor='center')

    def get_selected_columns(self):
        """
        Store the currently selected columns from both listboxes.
        
        Updates the internal _selected_features and _selected_target lists with
        the current selections from the respective listboxes.
        """
        self._selected_features = [self._feature_listbox.get(i) for i in self._feature_listbox.curselection()]
        self._selected_target = [self._target_listbox.get(i) for i in self._target_listbox.curselection()]

class MethodMenu:
    """
    A menu for selecting and applying methods to handle NaN values in data.
    
    This class provides a GUI interface for selecting different methods to handle
    missing values in the dataset. It includes a dropdown menu for method selection
    and additional inputs for specific methods like constant value filling.
    
    Attributes:
        METHODS : tuple
            Available methods for handling NaN values.
        _frame : tk.Frame
            The main frame where widgets will be placed.
        _manager : MenuManager
            Controller object that handles the data processing logic.
        _method_var : tk.StringVar
            Variable holding the currently selected method.
        _method_dropdown : ttk.Combobox
            Dropdown widget for method selection.
        _constant_label : tk.Label
            Label for constant value input field.
        _constant_value_input : tk.Entry
            Entry widget for constant value input.
        _apply_button : tk.Button
            Button to apply the selected method.
    """
    # Constant: Methods for dealing with NaNs
    METHODS = ("Delete Rows", "Fill with Mean", 
                "Fill with Median", "Fill with a Constant Value")
    
    def __init__(self, frame, manager):
        """
        Initialize the method selection menu.
        
        Parameters:
            frame (tk.Frame): Parent frame where widgets will be placed.
            manager (MenuManager): Controller object for handling method application logic.
        """
        self._frame = frame
        self._manager = manager
        self._method_var = tk.StringVar()

        self.create_nan_selector()
        self._apply_button = self.create_apply_button()

    @property 
    def method_var(self):
        """
        Get the currently selected method.
        
        Returns:
            tk.StringVar: Variable containing the selected NaN handling method.
        """
        return self._method_var
    
    @property
    def constant_value_input(self):
        return self._constant_value_input.get()
    
    def create_nan_selector(self):
        """
        Create the NaN handling method selector.
        
        Creates a combobox for method selection and additional widgets for
        constant value input when needed. Includes appropriate labels and
        styling.
        """
        label = tk.Label(self._frame, text="Select a method to handle NaN:", fg = '#4d598a', bg = '#d0d7f2',font= ("DejaVu Sans Mono", 10,'bold'))
        label.place(relx=0.5, rely=0.59, anchor="center")

        self._method_dropdown = ttk.Combobox(self._frame, textvariable=self._method_var, state="disabled", width=30)
        # textvariable=self._method_var: binds the dropdown to the variable self._method_var
        # The selected value is automatically updated in self._method_var
      
        self._method_dropdown['values'] = ("Delete Rows", "Fill with Mean", "Fill with Median", "Fill with a Constant Value")
        self._method_dropdown.place(relx=0.5, rely=0.67, relwidth=0.5, anchor="center")
        self._method_dropdown.bind("<<ComboboxSelected>>", self.toggle_cte_input)
        
        self._constant_label = tk.Label(self._frame, text="Introduce the constant:", fg = '#4d598a', bg = '#d0d7f2')
        self._constant_value_input = tk.Entry(self._frame, width=10, state="disabled")

        self._constant_value_input.place_forget()  # Hide it initially
        self._constant_label.place_forget()

        separator = tk.Frame(self._frame, bg = '#6677B8', height=3)
        separator.pack(fill = tk.X, side='bottom' )


    def toggle_cte_input(self, event):
        """
        Enables or disables the input field for a constant value
        based on the selected method.

        Parameters:
            event (tk.Event): The event triggered by method selection change.
        """
        # Every time you change the processing mode it locks the regression button to 
        # force you to press accept and use the most up-to-date selection.
        self._manager.disable_regression_button()

        selected_method = self._method_var.get()

        if selected_method == "Fill with a Constant Value": 
            self._constant_label.place(relx=0.45, rely=0.73, anchor="center")
            self._constant_value_input.place(relx=0.6, rely=0.73, anchor="center")
            self._constant_value_input.config(state="normal")
            self._constant_value_input.bind("<KeyRelease>", lambda event: self._manager.disable_regression_button())
        else:
            self._constant_label.place_forget()
            self._constant_value_input.place_forget()  # Hide it initially 
            self._constant_value_input.delete(0, "end")
            self._constant_value_input.config(state="disabled")

        if selected_method:
            self._apply_button.config(state="normal")
        else:
            self._apply_button.config(state="disabled")

    def create_apply_button(self):
        """
        Create the button to apply the selected NaN handling method.
        
        Returns:
            tk.Button: The configured apply button widget.
        """
        apply_button = tk.Button(self._frame, text="Apply", command=self._manager.apply_nan_handling, state="disabled",
                                 font=("Arial", 10,'bold'), fg="#FAF8F9", bg = '#6677B8' , activebackground="#808ec6",
                                 activeforeground="#FAF8F9", cursor="hand2" )
        apply_button.place(relx=0.5, rely=0.80, anchor="center")
        return apply_button

    def enable_selector(self):
        """Enable the method selection dropdown."""
        self._method_dropdown["state"] = "readonly"

    def disable_selector(self):
        """Disable the method selection dropdown and clear current selection."""
        self._method_var.set("")  # Clears the selected value 
        self._method_dropdown["state"] = "disabled"

    def display_nan_message(self, message):
        """
        Display a message about NaN values.
        
        Parameters:
            message (str): The message to display.
        """
        self._message_label.config(text=message)

    def clear_nan_message(self):
        """Clear the NaN message display."""
        self._message_label.config(text="")

class MenuManager:
    """
    Manager class for coordinating column selection and NaN handling interfaces.
    
    This class manages the interaction between the column selection menu and the
    NaN handling menu, coordinates data preprocessing, and handles the creation
    of the linear regression model.
    
    Attributes:
        METHOD_NAMES : tuple
            Available methods for handling NaN values.
        _app : object
            The main application instance.
        _frame : tk.Frame
            The main frame containing all menu components.
        _columns : list
            List of available column names.
        _df : pd.DataFrame
            The original DataFrame.
        _new_df : pd.DataFrame or None
            The preprocessed DataFrame.
        _chart_frame : tk.Frame
            Frame for displaying the regression chart.
        _column_menu : ColumnMenu
            Interface for column selection.
        _method_menu : MethodMenu
            Interface for NaN handling method selection.
        _regression_button : tk.Button
            Button to trigger regression model creation.
    """

    METHOD_NAMES = ("Delete Rows", "Fill with Mean", 
               "Fill with Median", "Fill with a Constant Value")
    
    def __init__(self, app, frame, columns, df, chart_frame):
        """Initialize the menu manager.
        
        Parameters:
            app : object
                The main application instance.
            frame : tk.Frame
                The main frame for menu components.
            columns : list
                List of available column names.
            df : pd.DataFrame
                The input DataFrame.
            chart_frame : tk.Frame
                Frame for displaying the regression chart.
        """
        self._app = app  # We only use it to update the scroll area 

        self._frame = frame
        self._columns = columns
        self._df = df
        self._new_df = None  # DataFrame where the preprocessed data will be

        self._chart_frame = chart_frame  # Frame where the graphic will be 

        self._column_menu = ColumnMenu(self._frame, columns, self)
        self._method_menu = MethodMenu(self._frame, self)
        self.create_regression_button()

        # To update the scroll area
        # This function must be called whenever we create a new widget
        # (It will have to be called again after generating the graph)
        self._app.scroll_window.update()

        print("df Before pre-processing")
        print(self._df)

        print("new_df Before pre-processing")
        print(self._new_df)

    @property
    def df(self):
        return self._df
    
    @property
    def new_df(self):
        return self._new_df
    
    def on_select(self, event):
        """
        Handle selection events from the column listboxes.
        Disables the method selector and regression button when column selection changes.
        
        Parameters
            event (tk.Event): The selection event from the listbox.
        """
        self._method_menu.disable_selector()
        self.disable_regression_button()

    def create_regression_button(self):
        """
        Create the button for initiating linear regression model creation.
        Creates and places a styled button that triggers the linear regression
        model creation process. The button is initially disabled.
        """
        self._regression_button = tk.Button(self._frame, text="Create Linear Regression Model", 
                                       command=self.create_linear_model,
                                       state = "disabled",  # Empieza deshabilitado
                                       font=("Arial", 10, 'bold'), fg="#FAF8F9", 
                                       bg='#6677B8', activebackground="#808ec6",
                                       activeforeground="#FAF8F9", cursor="hand2")
        self._regression_button.place(relx=0.5, rely=0.93, anchor='center')

    def enable_regression_button(self):
        """Enable the regression model creation button."""
        self._regression_button.config(state="normal")

    def disable_regression_button(self):
        """Disable the regression model creation button."""
        self._regression_button.config(state="disabled")

    def confirm_selection(self):
        """
        Validate and confirm the column selection.
        
        Updates the selected features and target variables, checks for NaN values
        in the selected columns, and enables/disables the appropriate interface
        elements based on the presence of NaN values.
        
        Displays appropriate message boxes for errors and success confirmations.
        """
        # Updates the selected_features and selected_target variables of 
        # ColumnMenu with the current selection
        self._column_menu.get_selected_columns()

        # Obtains the ColumnMenu selection 
        selected_features = self._column_menu.selected_features
        selected_target = self._column_menu.selected_target

        if len(selected_features) == 0:
            messagebox.showerror("Error", "You must select an input column (feature).")

        elif len(selected_target) == 0:
            messagebox.showerror("Error", "You must select an output column (target).")
        
        else:
            f_cols = ', '.join(selected_features)
            t_col = ', '.join(selected_target)
            success_window = messagebox.showinfo("Success", f"Feature: {f_cols}\nTarget: {t_col}")
            
            if success_window == 'ok':
                # Create an instance of the NanHandler object after having the columns selected 
                self._nan_handler = NaNHandler(self._df, MenuManager.METHOD_NAMES, 
                                         selected_features + selected_target)
                
                # Verify if there are null values in the selected columns 
                has_missing, nan_message = self._nan_handler.check_for_nan()
                
                messagebox.showinfo("Non-existent values", nan_message)
                if has_missing:
                    self._method_menu.enable_selector()  # Enable the selector if there are null values 
                    self.disable_regression_button()  # Disable it if the columns change
                else:
                    self._method_menu.disable_selector() # Disable the selector if there are no null values 
                    self.enable_regression_button()  # Allows the model to be created 

    def apply_nan_handling(self):
        """
        Apply the selected NaN handling method to the data.
        
        Processes the data using the selected method and constant value (if applicable).
        Handles validation of constant values and displays appropriate error messages.
        Enables the regression button if preprocessing is successful.
        
        Raises:
            ValueError: If the constant value input is not a valid number.
            ConstantValueError: If there's an error with the constant value handling.
        """
        method = self._method_menu.method_var.get()
        constant_value = self._method_menu.constant_value_input
        
        # It will be empty if nothing has beeen entered (because another method was chosen or because it was not entered it when it was due).
        if constant_value is None or constant_value.strip() == "":
            constant_value = None  # We make sure it is None if nothing was entered 
        else:
            try:
                constant_value = float(constant_value)  # Convert to float 
            except ValueError:
                messagebox.showerror("Error", "The constant value must be a number.")
                return  # We exit the method if it is not a valid number

        try:
            # We apply preprocessing with the selected method
            self._new_df = self._nan_handler.preprocess(method, constant_value)
        except ConstantValueError as e:
            messagebox.showerror("Error", str(e))
            return  # We exit the method if there is an error

        # If there are no errors, we show success and enable the regression button
        print("\ndf After pre-processing")
        print(self._df)

        print("\nnew_df Before pre-processing")
        print(self._new_df)

        messagebox.showinfo("Success", "Non-existent data handling has been successfully applied.")
        self.enable_regression_button()  # Allows the model to be created

    def create_linear_model(self):
        """
        Create and display the linear regression model.
        
        Creates a linear regression model using the selected feature and target columns.
        Validates data sufficiency and displays the regression results in the chart frame.
        
        Displays appropriate error messages if there are issues with the data or selection.
        """
        if len(self._column_menu.selected_features) == 0 or len(self._column_menu.selected_target) == 0:
            messagebox.showerror("Error", "You must select input and output columns before creating the model.")

        # Use the processed DataFrame if it exists, otherwise use the original
        df_to_use = self._new_df if self._new_df is not None else self._df

        # Get the first selected feature 
        feature = df_to_use[self._column_menu.selected_features[0]]
        target = df_to_use[self._column_menu.selected_target[0]]

        # Check if there is enough data to create the model
        if len(feature) < 2 or len(target) < 2:
            messagebox.showerror("Error", "There isn't enough data to create the regression model.")

        # Show success message and wait for confirmation
        success = messagebox.showinfo("Success", "The linear regression model will be created successfully.\nPress OK to see the results.")
        
        if success == 'ok':
            self.clear_frame(self._chart_frame)  # We empty it if there is something

            # Create the regression model
            LinearRegressionInterface(self._chart_frame, feature, target)
            self._app.scroll_window.update()  #########
    
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
