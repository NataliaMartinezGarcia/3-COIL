import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from open_files import open_file, FileFormatError, EmptyDataError
from scroll_table import ScrollTable
from menu_manager import MenuManager
from model_handler import open_model
import model_interface
from progress_bar import run_with_loading

class ScrollApp:
    """Main application class that creates a scrollable window interface.
    
    Handles window creation, scrolling functionality, and file operations
    for the Linear Regression application.

    Parameters:
        - window (tk.Tk): The main Tkinter window object
    
    Returns:
        - ScrollApp: Instance of the ScrollApp class
    """

    MAX_PATH_LENGTH = 50  # Maximum length for displayed file paths
        
    def __init__(self, window: tk.Tk):
        """
        Initialize the ScrollApp with a main window.
        
        Parameters:
            - window (tk.Tk): The main Tkinter window object
        """
        self._file = None
        self._file_path = tk.StringVar() # Stores the current file path for display
        self._window = window
        # Setting up the main window and application structure
        self._setup_window()
        self._create_frames()
        self._setup_canvas()
        self._create_app()
        
        # Show introduction message
        self._show_introduction()
    

    def _setup_window(self):
        """
        Configure main window properties.
        Calculates window dimensions based on screen size and centers the window.
        """
        # Set up window close handler
        self._window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self._window.title("Linear Regression App")
        
        # Fixed window size
        self._width = 768
        self._height = 576
        
        # Calculate position to center window
        self._x = (self._window.winfo_screenwidth() - self._width) // 2
        self._y = (self._window.winfo_screenheight() - self._height) // 2

        # Apply geometry settings
        self._window.geometry(f"{self._width}x{self._height}+{self._x}+{self._y}")

    def _create_frames(self):
        """Create main application frames."""
        self._main_frame = tk.Frame(self._window)
        self._main_frame.pack(fill="both", expand=True)
        
        # Create header before scroll area
        self._create_header()
    

    def _setup_canvas(self):
        """Set up scrollable canvas and related widgets."""
        # Create main canvas for scrollable content
        self._my_canvas = tk.Canvas(self._main_frame)
        self._my_canvas.pack(side="left", fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self._main_frame,
            orient="vertical",
            command=self._my_canvas.yview  # Link scrollbar to canvas vertical scroll
        )
        scrollbar.pack(side="right", fill="y")
        
        # Configure canvas
        self._my_canvas.configure(yscrollcommand=scrollbar.set)
        # Update scroll region when canvas size changes
        self._my_canvas.bind(
            "<Configure>",
            lambda e: self._my_canvas.configure(scrollregion=self._my_canvas.bbox("all"))
        )
        
        # Create frame for content with blue background
        self._second_frame = tk.Frame(self._my_canvas, bg='#d0d7f2')
        # Place content frame at top-left of canvas
        self._my_canvas.create_window((0, 0), window=self._second_frame, anchor="nw")
    

    def _create_app(self):
        """Create main application instance."""
        self._app = App(self._second_frame, self._my_canvas, self)
    

    def _create_header(self):
        """Create application header with file controls."""
        header_frame = tk.Frame(
            self._main_frame,
            bg='#d0d7f2',
            height=40,
            width=682
        )
        header_frame.pack(fill=tk.X, side='top')
        header_frame.pack_propagate(False)
        
        # Path label
        self._create_path_label(header_frame)
        
        # File path display
        self._create_path_display(header_frame)
        
        # Control buttons
        self._create_control_buttons(header_frame)
        
        # Separator
        separator = tk.Frame(self._main_frame, bg='#6677B8', height=3)
        separator.pack(fill=tk.X, side='top')
    

    def _create_path_label(self, parent):
        """
        Create 'PATH' label in header.
        Parameters:
            - parent: Parent frame to contain the label
        """
        label = tk.Label(
            parent,
            text='PATH',
            fg='#6677B8',
            bg="#d0d7f2",
            font=("DejaVu Sans Mono", 13, 'bold')
        )
        label.pack(side='left', padx=(10, 5), pady=5)
    

    def _create_path_display(self, parent):
        """
        Create file path display label.

        Parameters:
            - parent: Parent frame to contain the display
        """
        self._file_path.set("  Open a file by clicking 'Open' or load a model by clicking 'Load'  ")
        path_label = tk.Label(
            parent,
            textvariable=self._file_path,
            fg="#FAF8F9",
            bg='#6677B8',
            font=("DejaVu Sans Mono", 11),
            width=52
        )
        path_label.pack(side='left', padx=(20, 0), pady=5)
    

    def _create_control_buttons(self, parent):
        """
        Create 'Load' and 'Open' buttons.

        Parameters:
            - parent: Parent frame to contain the buttons
        """
        # Load button
        load_button = self._create_button(
            parent,
            "Load",
            self.search_model
        )
        load_button.pack(side='right', padx=(0, 20), pady=5)
        
        # Open button
        open_button = self._create_button(
            parent,
            "Open",
            self.search_file
        )
        open_button.pack(side='right', padx=(10, 20), pady=5)
    
    def _create_button(self, parent, text, command):
        """Create a styled button.
        
        Parameters:
            - parent : Parent frame to contain the button
            - text: Button label text
            - command: Function to execute when button is clicked
            
        Returns:
            - tk.Button: Created button widget
        """
        return tk.Button(
            parent,
            text=text,
            font=("Arial", 12, 'bold'),
            fg="#FAF8F9",
            bg='#6677B8',
            activebackground="#808ec6",
            activeforeground="#FAF8F9",
            cursor="hand2",
            command=command,
            padx=10,
            pady=10,
            width=5
        )
    
    def search_file(self, event=None):
        """
        Open file dialog to select and load a data file.
        
        Parameters:
            - event: Optional event parameter for binding to GUI elements
        """
        # Define allowed file types
        filetypes = (
            ("Compatible files (CSV, EXCEL, SQL)", "*.csv *.xlsx *.xls *.db *.sqlite"),
        )
        
        # Open file dialog
        self._file = filedialog.askopenfilename(
            title="Search file",
            filetypes=filetypes
        )
        
        if not self._file:
            messagebox.showwarning("Warning", "You haven't selected any files.")
            return
            
        try:
            # Wrap file loading process in a function for progress bar
            def full_load_process():
                self._data = open_file(self._file)  # Read file data
                self._app.data = self._data  # Update app data
                self._app.prepare_data_display()  # Prepare UI
                return self._data

             # Display loading progress while processing file
            run_with_loading(
                self._window,
                full_load_process,
                "Reading and opening file..."
            )
                
             # Update file path display with shortened path
            text = self._shorten_route_text(self._file)
            self._file_path.set(text)
            messagebox.showinfo("Success", "The file has been read correctly.")
            
            # Display the processed data in the UI
            self._app.show_prepared_data()
            
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"The file could not be found: {str(e)}")
        except FileFormatError as e:
            messagebox.showerror("Error", f"Invalid format: {str(e)}")
        except EmptyDataError as e:
            messagebox.showwarning("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"The file could not be loaded: {str(e)}")
        
    def _update_interface_with_file(self):
        """Update interface after successful file load."""
        text = self._shorten_route_text(self._file)
        self._file_path.set(text)
        
        messagebox.showinfo("Success", "The file has been read correctly.")

    def search_model(self, event=None):
        """
        Open file dialog to select and load a model file.

        Parameters:
            - event: Optional event parameter for binding to GUI elements
        """
        filetypes = (
            ("Compatible files (pickle, joblib)", "*.pkl *.joblib"),
        )
        self._file = filedialog.askopenfilename(
            title="Load model",
            filetypes=filetypes
        )
        
        if not self._file:
            messagebox.showwarning("Warning", "You haven't selected any files.")
            return
            
        try:
            def full_load_process():
                # Load and preprocess the model
                self._data = open_model(self._file)
                self._app.data = self._data
                self._app.prepare_model_display()
                return self._data

           # Run loading process with progress indicator
            run_with_loading(
                self._window,
                full_load_process,
                "Loading and processing model..."
            )
            
           # Update the interface and show success message
            text = self._shorten_route_text(self._file)
            self._file_path.set(text)
            messagebox.showinfo("Success", "The file has been read correctly.")
            
             # Show the prepared model
            self._app.show_prepared_model()
            
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"The file could not be found: {str(e)}")
        except AssertionError as e:
            messagebox.showerror("Error", f"Invalid format: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"The file could not be loaded: {str(e)}")

    def _shorten_route_text(self, text):
        """
        Truncate file path if it exceeds maximum length.
        
        Parameters:
            - text: Full file path to be shortened
            
        Returns:
            - str: Shortened file path if necessary, original path otherwise
        """
        if len(text) > self.MAX_PATH_LENGTH:
            return "..." + text[-self.MAX_PATH_LENGTH:]
        return text
    
    def _show_introduction(self):
        """Show welcome message with usage instructions."""
        messagebox.showinfo(
            "Welcome!",
            "To use this app correctly, follow these steps:\n\n"
            "1) Open a file / model from your computer with the buttons\n\n"
            "2) Select your feature and target columns\n\n"
            "3) If they have non-existent values, handle them before creating the model\n\n"
            "4) Press Create Linear Regression to see the graph and the model information\n\n"
            "You can save your model by pressing Download and add a comment of your choice.\n\n"
            "If you'd like to change your selections at any point you can always go back and follow the steps again."
        )
    
    def update(self):
        """Update canvas scroll region."""
        self._second_frame.update_idletasks()
        self._my_canvas.configure(scrollregion=self._my_canvas.bbox("all"))
    
    def on_closing(self):
        """Handle window closing event."""
        self._window.quit()
        self._window.destroy()
    
    @property
    def window(self):
        """Get main window instance."""
        return self._window

class App:
    """
    Main application logic class handling data display and processing.
    
    Parameters:
        - frame: Main application frame
        - canvas: Scrollable canvas for content
        - scroll_window: Parent ScrollApp instance
        
    Returns:
        - App: Instance of the App class
    """
    
    def __init__(self, frame: tk.Frame, canvas: tk.Canvas, scroll_window: ScrollApp):
        """
        Initialize App with necessary frames and canvas.
        
        Parameters:
            - frame: Main application frame
            - canvas: Scrollable canvas for content
            - scroll_window: Parent ScrollApp instance
        """
        self._table_frame = tk.Frame()
        self._frame = frame
        self._canvas = canvas
        self._scroll_window = scroll_window
        # Bind window resize handler
        self._scroll_window.window.bind("<Configure>", self.on_window_resize)
        
        self._table = None
        self._file = None
        self._file_path = tk.StringVar()
        self._data = None
        self._processed_data = None
    
    @property
    def data(self):
        """Get current data."""
        return self._data
    
    @data.setter
    def data(self, df):
        """Set current data."""
        self._data = df
    
    @property
    def scroll_window(self):
        """Get scroll window instance."""
        return self._scroll_window
    
    def show_data(self):
        """Display data in table format."""
        self.clear_frame()
        self._create_table_frame()  # Create table frame
        self._create_table()  # Create and populate table
        self._create_separator()  # Create separator
        self._setup_column_selection()  # Setup column selection
        self.prepare_data_display()
        self.show_prepared_data()

    def prepare_data_display(self):
        """
        Prepare data for display without updating the interface.
        Clears existing content and sets up new table with loaded data.
        """
        self.clear_frame()
        
        # Create table frame
        self._create_table_frame()
        
        # Create new table instance and populate with data
        self._table = ScrollTable(self._table_frame)
        self._table.empty_table()  # Clear any existing data
        self._table.create_from_df(self._data)  # Fill with new data

    def show_prepared_data(self):
        """Show the prepared data in the interface."""
        # Show the table
        self._table.show()
        
        # Create separator
        self._create_separator()
        
        # Setup column selection
        self._setup_column_selection()

    def _create_table_frame(self):
        """Create frame for data table."""
        self._table_frame = tk.Frame(
            self._frame,
            height=400,
            width=self._scroll_window.window.winfo_width() - 15
        )
        self._table_frame.pack(side=tk.TOP, fill=tk.X, anchor="center")
        self._table_frame.pack_propagate(False)
    
    def _create_table(self):
        """Create and populate data table."""
        self._table = ScrollTable(self._table_frame)
        self._table.empty_table()
        self._table.create_from_df(self._data)
        self._table.show()
    
    def _create_separator(self):
        """Create separator line."""
        separator = tk.Frame(self._frame, bg='#6677B8', height=3)
        separator.pack(fill=tk.X, side=tk.TOP, anchor="center")
    
    def _setup_column_selection(self):
        """
        Set up column selection interface for data analysis.
        
        Creates frames for column selection and chart display,
        initializes MenuManager for handling column operations.
        """
        # Get columns that contain numeric data
        numeric_columns = self._table.numeric_columns()
        
        # Create frame for column selection UI
        column_selector_frame = tk.Frame(
            self._frame,
            height=400,
            width=self._scroll_window.window.winfo_width() - 15,
            bg='#d0d7f2'
        )
        column_selector_frame.pack(fill=tk.BOTH, side=tk.TOP, anchor="center")
        column_selector_frame.pack_propagate(False)
        # Create frame for chart display
        chart_frame = tk.Frame(self._frame, bg='#d0d7f2')
        chart_frame.pack(fill=tk.BOTH, side=tk.TOP, anchor="center")
        
        # Initialize menu manager with column data
        self._menu = MenuManager(
            self,
            column_selector_frame,
            numeric_columns,
            self._data,
            chart_frame
        )
        self._processed_data = self._menu.new_df
    
    def show_model(self):
        """Display loaded model information."""
        self.prepare_model_display()
        self.show_prepared_model()

    def prepare_model_display(self):
        """Prepare model information for display."""
        try:
            self._model_info = self._extract_model_info()
            self.clear_frame()
            
            self._info_frame = tk.Frame(
                self._frame,
                height=self._scroll_window.window.winfo_height() - 50,
                width=self._scroll_window.window.winfo_width() - 15,
                bg='#d0d7f2'
            )
            self._info_frame.pack(side=tk.TOP, fill=tk.X, anchor="center")
            self._info_frame.pack_propagate(False)
        except:
            raise Exception("The file is not in a valid format.")

    def show_prepared_model(self):
        """Display prepared model information."""
        model_interface.show(
            self._info_frame,
            self._model_info["feature_name"],
            self._model_info["target_name"],
            self._model_info["intercept"],
            self._model_info["slope"],
            self._model_info["r_squared"],
            self._model_info["mse"],
            self._model_info["description"]
        )
        
        self._scroll_window.update()

    def _extract_model_info(self):
        """
        Extract model information from data.

        Returns:
            - dict: Dictionary containing model parameters and statistics
                   Including feature_name, target_name, intercept, slope,
                   r_squared, mse, and description
        """
        # Retrieve all model parameters and statistics from data dictionary
        return {
            "feature_name": self.data.get("feature_name"),  # Independent variable name
            "target_name": self.data.get("target_name"),    # Dependent variable name
            "intercept": self.data.get("intercept"),        # Y-intercept of regression line
            "slope": self.data.get("slope"),                # Slope of regression line
            "r_squared": self.data.get("r_squared"),        # R-squared value (model fit)
            "mse": self.data.get("mse"),                    # Mean Squared Error
            "description": self.data.get("description")     # User-provided description
        }
    
    def _show_model_info(self, model_info):
        """Display model information in interface."""
        info_frame = tk.Frame(
            self._frame,
            height=self._scroll_window.window.winfo_height() - 50,
            width=self._scroll_window.window.winfo_width() - 15,
            bg='#d0d7f2'
        )
        info_frame.pack(side=tk.TOP, fill=tk.X, anchor="center")
        info_frame.pack_propagate(False)
        
        model_interface.show(
            info_frame,
            model_info["feature_name"],
            model_info["target_name"],
            model_info["intercept"],
            model_info["slope"],
            model_info["r_squared"],
            model_info["mse"],
            model_info["description"]
        )
        
        self._scroll_window.update()
    
    def clear_frame(self):
        """Remove all widgets from main frame."""
        for widget in self._frame.winfo_children():
            widget.destroy()
    
    def on_window_resize(self, event):
        """
        Handle window resize events
        
        Parameters:
            - event: Window resize event object
        """
        if hasattr(self, '_table_frame') and self._table_frame.winfo_exists():
            self._table_frame.config(
                width=self._scroll_window.window.winfo_width() - 15
            )

def main():
    """Main application entry point."""
    window = tk.Tk()
    app = ScrollApp(window)
    window.mainloop()

if __name__ == "__main__":
    main()