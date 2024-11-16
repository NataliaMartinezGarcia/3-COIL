import tkinter as tk  
from tkinter import messagebox, filedialog, ttk  
import pandas as pd
from open_files import open_file, FileFormatError, EmptyDataError
from scroll_table import ScrollTable
from column_menu import MenuManager
from model_handler import open_model
import model_interface

class ScrollApp:
    """
    Main application class that creates a scrollable window interface.
    
    This class handles the main window creation, scrolling functionality,
    and file operations for the Linear Regression application.

    Attributes:
        _file (str): Path to the currently loaded file
        _file_path (StringVar): Tkinter variable to display the file path
        _window (tk.Tk): Main application window
        _width (int): Window width based on screen size
        _height (int): Window height based on screen size
        _x (int): Window x position for centering
        _y (int): Window y position for centering
        _main_frame (tk.Frame): Main container frame
        _my_canvas (tk.Canvas): Canvas for scrollable content
        _second_frame (tk.Frame): Frame inside canvas for widgets
        _app (App): Instance of the App class containing main application logic
    """
    def __init__(self, window):
        """
        Initialize the ScrollApp with a main window.

        Args:
            window (tk.Tk): The main window of the application
        """

        self._file = None  # Variable to perform operations with the path
        self._file_path = tk.StringVar()  # Variable to show the path on screen
        self._window = window

        # Set shutdown protocol to stop mainloop completely
        self._window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Window dimensions based on screen size
        self._width = self._window.winfo_screenwidth() //2
        self._height = int(self._window.winfo_screenheight() / 1.5) 
        # So that it appears centered on the screen
        self._x = (self._window.winfo_screenwidth() - self._width) // 2  # Centered on width
        self._y = (self._window.winfo_screenheight() - self._height) // 2  # Centered on height

        self._window.title("Linear Regression App")
        self._window.geometry(f"{self._width}x{self._height}+{self._x}+{self._y}")

        # Create a main frame
        self._main_frame = tk.Frame(self._window)
        self._main_frame.pack(fill="both", expand=True)

        # Header is outside the scroll area
        self.header()

        # Create a canvas
        self._my_canvas = tk.Canvas(self._main_frame)
        self._my_canvas.pack(side="left", fill="both", expand=True)

        # Add a scrollbar to the canvas 
        my_scroll_bar = ttk.Scrollbar(self._main_frame, orient="vertical", command=self._my_canvas.yview)
        my_scroll_bar.pack(side="right", fill="y")

        # Set the canvas
        self._my_canvas.configure(yscrollcommand=my_scroll_bar.set)
        self._my_canvas.bind("<Configure>", lambda e: self._my_canvas.configure(scrollregion = self._my_canvas.bbox("all")))

        # Create another frame inside the canvas 
        # This is where the rest of the widgets are added
        self._second_frame = tk.Frame(self._my_canvas, bg = '#d0d7f2')
        
        # Add the new frame to the window inside the canvas
        self._my_canvas.create_window((0, 0), window=self._second_frame, anchor="nw")
        # If we specify width and height in window = , the scroll area will have those dimensions
        # If not, it will adapt to the widgets inside it
        # Important: do not touch width, because it depends on the size of the table
        # and that frame adjusts itself when resizing the window
        #, width = self._width-13)

        # Main application with self._second_frame as main frame
        # We pass self._my_canvas to adjust the scroll area as widgets are added
        # We pass self to access the window dimensions from within the class and adjust the data table
        self._app = App(self._second_frame, self._my_canvas, self)

    # We need to access the window from another object to access its dimensions
    @property
    def window(self):
        """
        Get the main window instance.

        Returns:
            tk.Tk: The main window of the application
        """
        return self._window
    
    def search_file(self, event=None):
        """
        Open a file dialog to select and load a data file.
        
        Handles CSV, Excel, and SQL files. Updates the interface with the loaded data
        and displays appropriate success or error messages.

        Args:
            event: Optional event parameter for binding to widgets
        """
        filetypes = (
            ("Compatible files (CSV, EXCEL, SQL)", "*.csv *.xlsx *.xls *.db *.sqlite"),
        )
        self._file = filedialog.askopenfilename(
            title="Search file",
            filetypes=filetypes,
        )

        if self._file:
            try:
                # Open the files and updates the data 
                self._data = open_file(self._file)
                
                # Update the file's path in the interface 
                text = self.shorten_route_text(self._file)
                self._file_path.set(text)
                
                # Success message 
                messagebox.showinfo("Success", "The file has been read correctly.")

                # Update the data in the application and displays it
                self._app.data = self._data
                self._app.show_data()  # Call show_data with the DataFrame loaded

            except FileNotFoundError as e:
                messagebox.showerror("Error", f"The file could not be found: {str(e)}")
            except FileFormatError as e:
                messagebox.showerror("Error", f"Invalid format: {str(e)}")
            except EmptyDataError as e:
                messagebox.showwarning("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"The file could not be loaded: {str(e)}")
        else:
            messagebox.showwarning("Warning", "You haven't selected any files.")

    def search_model(self,event = None):
        """
        Open a file dialog to select and load a model file.
        
        Handles pickle and joblib files. Updates the interface with the loaded model
        and displays appropriate success or error messages.

        Args:
            event: Optional event parameter for binding to widgets
        """
        filetypes = (
            ("Compatible files (pickle, joblib)", 
            "*.pkl *.joblib"),
            )
        self._file = filedialog.askopenfilename(
            title="Load model",
            filetypes=filetypes) 

        if self._file:
        
            try: 
                self._data = open_model(self._file)
                text = self.shorten_route_text(self._file)
                self._file_path.set(text)

            except FileNotFoundError as e:
                messagebox.showerror("Error", f"The file could not be found: {str(e)}")

            except AssertionError as e:
                messagebox.showerror("Error", f"Invalid format: {str(e)}")
            
            except Exception as e:
                messagebox.showerror("Error", f"The file could not be loaded: {str(e)}")

            else:  # Si todo ha ido bien
                self._app.data = self._data
                self._app.show_model()

        else:  # Si no ha elegido un archivo
            messagebox.showwarning("Warning", "You haven't selected any files.")

    def shorten_route_text(self, text):
        """
        Truncate the file path text if it exceeds maximum length.

        Args:
            text (str): The full file path

        Returns:
            str: Truncated file path with ellipsis if necessary
        """
        max_chars = 50

        if len(text) > max_chars:
            truncated_text = "..." + text[-max_chars:]
        else:
            truncated_text = text

        return truncated_text
    
    def introduction(self):
        messagebox.showinfo("Welcome !", "To use this app correctly, follow these steps:"
                            "\n\n 1 ) Open a file / model from your computer with the buttons"
                            "\n\n 2 ) Select your feature and target columns"
                            "\n\n 3 ) If they have non-existent values, handle them before creating the model"
                            "\n\n 4 ) Press Create Linear Regression to see the graph and the model information"
                            "\n\n You can save your model by pressing Download and add a comment of your choice."
                            "\n\n If you'd like to change your selections at any point you can always go back and follow the steps again.")

    
    def header(self):
        """
        Create the header section of the application.
        
        Contains the file path display, open file button, and load model button.
        """
        # A frame is created to place the path label, the file path and the open button
        header_frame = tk.Frame(self._main_frame, bg = '#d0d7f2', height = 40, width = 682)
        header_frame.pack(fill = tk.X, side='top')
        header_frame.pack_propagate(False)

        label = tk.Label(header_frame, text= 'PATH' ,fg = '#6677B8',bg= "#d0d7f2", font= ("DejaVu Sans Mono", 13, 'bold'))
        label.pack(side='left',padx= (10,5) , pady=5)

        # Variable to store the path of the selected file and button to select it
        self._file_path.set("  Open a file by clicking 'Open' or load a model by clicking 'Load'  ")
        path_label = tk.Label(header_frame, textvariable= self._file_path, fg= "#FAF8F9", bg = '#6677B8',
                                font= ("DejaVu Sans Mono", 11), width = 52)
        path_label.pack(side='left',padx=(20,0), pady=5)

        load_button = tk.Button(header_frame, text="Load", font=("Arial", 12,'bold'),
                                  fg="#FAF8F9", bg = '#6677B8' ,activebackground="#808ec6",activeforeground="#FAF8F9",
                                  cursor="hand2" , command=self.search_model, padx=10, pady=10, width = 5)
        load_button.pack(side='right',padx = (0,20), pady=5) 

        # Button to open the file explorer
        search_button = tk.Button(header_frame, text="Open", font=("Arial", 12,'bold'),
                                  fg="#FAF8F9", bg = '#6677B8' ,activebackground="#808ec6",activeforeground="#FAF8F9",
                                  cursor="hand2", command= self.search_file , padx=10, pady=10,width = 5)
        search_button.pack(side='right',padx = (10,20), pady=5) 

        # A separator line for aesthetics
        separator = tk.Frame(self._main_frame, bg = '#6677B8', height=3)
        separator.pack(fill = tk.X, side='top')

        self._main_frame.pack(fill=tk.BOTH, expand=True)
        self.introduction()

    def update(self):
        """
        Update the scroll region of the canvas.
        
        Called after adding new widgets to ensure proper scrolling functionality.
        """
        # Updates the graphical interface before adjusting the scroll region
        self._second_frame.update_idletasks()
        # Update scroll region after adding new buttons
        self._my_canvas.configure(scrollregion=self._my_canvas.bbox("all"))

    def on_closing(self):
        """
        Handle the window closing event.
        
        Stops the mainloop and destroys the window, completely stopping the execution of the program.
        """
        self._window.quit()  # Stop Tkinter mainloop
        self._window.destroy()  # Close the window

########################################################################################

# Main class to manage the graphical interface
class App:
    """
    Main application logic class handling data display and processing.
    
    This class manages the data table, column selection, and chart display
    functionality of the application.

    Attributes:
        _frame (tk.Frame): Main container frame
        _canvas (tk.Canvas): Canvas for scrollable content
        _scroll_window (ScrollApp): Reference to parent ScrollApp instance
        _table (ScrollTable): Data table widget
        _file (str): Currently loaded file path
        _file_path (StringVar): Tkinter variable for file path display
        _data (pd.DataFrame): Original unmodified data
        _processed_data (pd.DataFrame): Data after preprocessing
    """

    # IN THE FUTURE, GETTERS WILL HAVE TO BE MADE FOR THE ATTRIBUTES THAT NEED IT
    def __init__(self, frame, canvas, scroll_window):
        """
        Initialize the App with necessary frames and canvas.

        Args:
            frame (tk.Frame): Main container frame
            canvas (tk.Canvas): Canvas for scrollable content
            scroll_window (ScrollApp): Reference to parent ScrollApp instance
        """

        # Frame where the table will go
        # It is actually redefined later, but it must be initialized before adding the
        # event to the window because if not an error appears saying that it does not exist
        self._table_frame = tk.Frame()  

        self._frame = frame
        self._canvas = canvas

        self._scroll_window = scroll_window
        # Event when window is resized
        self._scroll_window.window.bind("<Configure>", self.on_window_resize)
        
        self._table = None # Future object Table

        self._file = None  # Variable to perform operations with the path
        self._file_path = tk.StringVar()  # Variable to display the path on screen

        # DataFrame that will never be modified
        # Only overwritten when a new file is chosen
        self._data = None  
        # DataFrame with preprocessed data
        # Overwritten when a different preprocessing method is chosen
        self._processed_data = None 
    
    @property
    def data(self):
        return self._data
    
    # To be able to update the DataFrame when reading the file from the ScrollApp class
    @data.setter
    def data(self, df):
        self._data = df

    @property
    def scroll_window(self):
        return self._scroll_window
    
    def show_data(self):  
        """
        Display the data in a table format.
        
        Creates a table with scrollbars and sets up the column selector
        and chart display areas.
        """
        # Clear the frame if there was already a table previously
        # (which happens when the user changes files)
        self.clear_frame()
    
        # We create a frame for the data table and the scroll bars
        self._table_frame = tk.Frame(self._frame, height = 400, width = self._scroll_window.window.winfo_width() - 15)  # Establecer dimensiones
        self._table_frame.pack(side= tk.TOP, fill= tk.X, anchor = "center")
        self._table_frame.pack_propagate(False)  # To use height as table height
        
        self._table = ScrollTable(self._table_frame)  # Table with scrollbars where the data appears

        self._table.empty_table()  # Clear the table in case it already had data
        self._table.create_from_df(self._data)  # Copy the data from the DataFrame to the table
        self._table.show()  # Displays the table 

        separator = tk.Frame(self._frame, bg = '#6677B8', height = 3)
        separator.pack(fill = tk.X, side = tk.TOP, anchor = "center")

        #  Numeric columns of the table 
        numeric = self._table.numeric_columns()

        # Create a frame for the column sleector 
        column_selector_frame = tk.Frame(self._frame, height = 400, width = self._scroll_window.window.winfo_width() - 15, bg = '#d0d7f2')
        column_selector_frame.pack(fill = tk.BOTH, side = tk.TOP, anchor = "center")
        column_selector_frame.pack_propagate(False)
        # If we set the frame size and make it so that it cannot be reduced (with propagate = False)
        # There is no need to change from place to pack in the column_menu module

        chart_frame = tk.Frame(self._frame,bg = '#d0d7f2')
        chart_frame.pack(fill = tk.BOTH, side = tk.TOP, anchor = "center")        
       
        # Instantiating the MenuManager
        self._menu = MenuManager(self, column_selector_frame, numeric, self._data, chart_frame)
        self._processed_data = self._menu.new_df  # Actualiza el df procesado
        
        # To update the scroll area
        # This function must be called whenever we create a new widget
        # (It will have to be called again after generating the graph)
        # self._scroll_window.update()
    
    def show_model(self): 
        """
        Display the loaded model information.
        
        Extracts and shows model parameters and statistics.
        """
        try:
            feature_name = self.data.get("feature_name")
            target_name = self.data.get("target_name")
            intercept = self.data.get("intercept")
            slope = self.data.get("slope")
            r_squared = self.data.get("r_squared")
            mse = self.data.get("mse")
            description = self.data.get("description")
        except:
            messagebox.showinfo("Error", "The file is not in a valid format.")               
            return

        messagebox.showinfo("Success", "The file has been read correctly.")               

        self.clear_frame()
               
        info_frame = tk.Frame(self._frame, height = self._scroll_window.window.winfo_height() - 50, width = self._scroll_window.window.winfo_width() - 15, bg = '#d0d7f2') 
        info_frame.pack(side= tk.TOP, fill= tk.X, anchor = "center")
        info_frame.pack_propagate(False) 

        model_interface.show(info_frame,feature_name,target_name,intercept,slope,r_squared,mse,description)
        
        self._scroll_window.update()

    def clear_frame(self):
        """
        Remove all widgets from the main frame.
        """
        for widget in self._frame.winfo_children():
            widget.destroy()

    def on_window_resize(self, event):
        """
        Handle window resize events.
        
        Updates the table frame width when the window is resized.

        Args:
            event: The window resize event
        """
        
        if hasattr(self, '_table_frame') and self._table_frame.winfo_exists():  # Comprueba que la tabla existe
            self._table_frame.config(width= self._scroll_window.window.winfo_width() - 15)

########################################################################################

# Para probar

def main():
    ventana = tk.Tk()  # Main window 
    app = ScrollApp(ventana)
    ventana.mainloop()  # Starts the main loop of the application

if __name__ == "__main__":
    main()