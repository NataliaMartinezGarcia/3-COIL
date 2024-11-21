import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
from tkinter import font

# Class to manage data table with slider bars.


class ScrollTable(ttk.Treeview):
    """
    A scrollable table widget that displays pandas DataFrame data.

    This class extends ttk.Treeview to create a table with both horizontal
    and vertical scrollbars. It provides methods to load and display
    DataFrame data with proper column sizing.

    Attributes
        _frame (ttk.Frame): The parent frame containing the table and scrollbars.
        _data (pandas.DataFrame): The DataFrame being displayed in the table.
        _scroll_x (tk.Scrollbar): Horizontal scrollbar for the table.
        _scroll_y (tk.Scrollbar): Vertical scrollbar for the table.
    """

    def __init__(self, frame):
        """
        Initialize the ScrollTable widget.

        Parameters
        frame (ttk.Frame): The parent frame to contain the table and scrollbars.
        """
        super().__init__(frame, columns=[], show="headings")
        self._frame = frame
        self._data = None  # At the time of creation, the table is empty

        # Creates table and scrollbars but they remain hidden until the table has data

        # Horizontal scroll bar
        self._scroll_x = tk.Scrollbar(self._frame, orient=tk.HORIZONTAL)

        # Vertical scroll bar
        self._scroll_y = tk.Scrollbar(self._frame, orient=tk.VERTICAL)

        # Connect scrollbars to existing table (self)
        self.config(xscrollcommand=self._scroll_x.set,
                    yscrollcommand=self._scroll_y.set)

        # Configure the scrollbars
        self._scroll_x.config(command=self.xview)
        self._scroll_y.config(command=self.yview)

        # self._frame.pack_propagate(True)

    @property  # DataFrame that the table shows
    def data(self):
        return self._data

    def empty_table(self):
        """Remove all items from the existing table."""
        self.delete(*self.get_children())

    def create_from_df(self, df):
        """
        Configure table columns and insert data from a DataFrame.

        Parameters:
            df (pandas.DataFrame): The DataFrame to display in the table.
        """
        self._data = df
        self['columns'] = list(df.columns)
        for col in df.columns:
            self.heading(col, text=col)
            self.column(col, anchor='center')

        for _, row in df.iterrows():
            self.insert("", "end", values=list(row))

    def show(self):
        """Display the table and scrollbars in the frame."""
        self._scroll_x.pack(
            side=tk.TOP, fill=tk.X)  # Horizontal bar at the top
        # Vertical bar on the right
        self._scroll_y.pack(side=tk.LEFT, fill=tk.Y)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Table
        self.adjust_width()

    def numeric_columns(self):
        """
        Get the names of columns containing numeric data.

        Returns:
            pandas.Index: Names of columns with numeric data types.
        """
        return self._data.select_dtypes(include=['number']).columns

    def adjust_width(self):
        """Adjust the width of each column based on content and header text."""
        for col in self["columns"]:
            # Obtain the header text
            heading = self.heading(col, "text")

            # Calculate the width of the header text
            column_font = font.Font()
            heading_width = column_font.measure(heading)

            # Obtain the first elemento of the column (if it exists):
            first_element = self.item(self.get_children()[0])[
                "values"][self["columns"].index(col)]

            # Calculate the width of the first element's text
            # For the content you have to add something because otherwise it will be very tight!
            first_element_width = column_font.measure(str(first_element)) + 15

            # Select the largest width between the header and the first element
            width = max(heading_width, first_element_width)

            # Assign final width to column
            self.column(col, width=width)


# Code to test the ScrollTable class
if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    root.title("Demo de ScrollTable")
    root.geometry("300x400")

    # Create a frame for the table
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Create a ScrollTable instance
    table = ScrollTable(frame)

    # Create sample data in a DataFrame with many rows and columns
    num_rows = 200  # Increase the number of rows
    num_columns = 10  # Increase the number of columns
    data = {
        "ID": np.arange(1, num_rows + 1),
        "Nombre": [f"Nombre {i}" for i in range(1, num_rows + 1)],
        "Edad": np.random.randint(18, 60, size=num_rows),
        "Ciudad": [f"Ciudad {i}" for i in range(1, num_rows + 1)],
        "Salario": np.random.randint(20000, 100000, size=num_rows),
        "Departamento": [f"Dep {i}" for i in range(1, num_rows + 1)],
        "Email": [f"email{i}@ejemplo.com" for i in range(1, num_rows + 1)],
        "Teléfono": [f"555-{i:04d}" for i in range(1, num_rows + 1)],
        "Fecha de Ingreso": pd.date_range(start='2020-01-01', periods=num_rows, freq='D').tolist(),
        # Evaluación de 1 a 5
        "Evaluación": np.random.randint(1, 6, size=num_rows)
    }

    df = pd.DataFrame(data)

    # Load the data in the table
    table.create_from_df(df)

    # Display the table
    table.show()

    # Start the main loop of the graphical interface
    root.mainloop()
