import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from linear_regression import LinearRegression
import statsmodels.api as sm
from model_handler import save_model
import model_interface


class LinearRegressionInterface:
    """
    A class that provides a graphical user interface for linear regression analysis.

    This class creates a visualization of the linear regression model, including the scatter plot
    of the data points, the regression line, and model statistics. It also provides functionality
    to save the model with an optional description.

    Attributes:
        _frame (tk.Frame): The main frame where the interface elements will be placed
        _feature (pd.Series): The independent variable (X) for the regression
        _target (pd.Series): The dependent variable (y) for the regression
        _comment (tk.Text): Text widget for model description input
        _linear_regression (LinearRegression): Object that handles the regression calculations
    """

    def __init__(self, frame, feature, target):
        """
        Initialize the LinearRegressionInterface with the provided data.

        Args:
            frame (tk.Frame): The main frame to contain the interface elements
            feature (pd.Series): The independent variable data
            target (pd.Series): The dependent variable data
        """
        self._frame = frame   # Main frame of the interface
        self._feature = feature  # Will be passed to the calculation class
        self._target = target
        self._comment = None
        self._prediction_frame = None # Will be used to make predictions based on the model

        # Create linear regression object for calculations and results
        self._linear_regression = LinearRegression(feature, target)

        # Create and display the plot in the interface
        self.create_plot()

    def create_plot(self):
        """
        Creates and displays the regression plot in the interface.

        The plot includes:
        - Scatter plot of the actual data points
        - Regression line
        - Axis labels and legend
        - Model statistics display
        """
        # Extract the necessary data for the plot
        predictions = self._linear_regression.predictions

        # Create matplotlib figure
        fig, ax = plt.subplots()
        # Change background color of the entire figure (light blue)
        fig.patch.set_facecolor('#d0d7f2')

        ax.scatter(self._feature, self._target, color='#808ec6',
                   label='Data', s=10)  # Real data points
        ax.plot(self._feature, predictions, color='#bc2716',
                label='Regression line', linewidth=2)  # Regression line
        ax.set_xlabel(self._linear_regression._feature_name, fontsize=8)
        ax.set_ylabel(self._linear_regression._target_name, fontsize=8)
        # Size of numbers on axes
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.legend(fontsize=8)

        # Integrate the figure into the tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self._frame)
        canvas.get_tk_widget().config(bg='#d0d7f2')
        canvas.draw()
        canvas.get_tk_widget().pack()

        model_interface.show(self._frame, self._linear_regression.feature_name, self._linear_regression.target_name, self._linear_regression.intercept,
                             self._linear_regression.slope, self._linear_regression.r_squared,
                             self._linear_regression.mse, None)

        self.predictions()

    def predictions(self):

        predictions_frame = tk.Frame(self._frame, height=250, bg='#d0d7f2')
        predictions_frame.pack(side = 'top')

        entry_frame = tk.Frame(predictions_frame, bg='#d0d7f2')
        entry_frame.pack(side = 'left')

         # Model predictions
        label = tk.Label(entry_frame, text='Enter a value to predict its output', fg='#4d598a', bg='#d0d7f2',
                         font=("DejaVu Sans Mono", 11, 'bold'))
        label.pack(side='top', padx=(10, 20), pady=5)

        self._prediction_frame = tk.Entry(entry_frame, width=10)
        self._prediction_frame.pack(side='top', padx=20, pady=5)

        prediction_button = tk.Button(predictions_frame, text="Predict", font=("Arial", 12, 'bold'),
                                fg="#FAF8F9", bg='#6677B8', activebackground="#808ec6", activeforeground="#FAF8F9",
                                cursor="hand2", command=self.predict)
        prediction_button.pack(side='left', padx = 10)

        self.comment()

    def comment(self):
        """
        Creates and displays the interface elements for adding a model description
        and downloading the model.

        This includes:
        - A text area for entering the model description
        - A download button to save the model
        """
        download_frame = tk.Frame(self._frame, height=250, bg='#d0d7f2')

        entry_frame = tk.Frame(download_frame, width=250,
                               height=250, bg='#d0d7f2')
        # Description
        label = tk.Label(entry_frame, text='Write a description for the model (optional)', fg='#4d598a', bg='#d0d7f2',
                         font=("DejaVu Sans Mono", 11, 'bold'), width=50)
        label.pack(side='top', fill='x', padx=(10, 20), pady=5)

        self._comment = tk.Text(entry_frame, width=30, height=5, font=(
            "Arial", 10, 'bold'), wrap="word")
        self._comment.pack(side='top', fill=tk.BOTH, padx=20, pady=5)

        entry_frame.pack(side='left', padx=40, pady=10)

        save_button = tk.Button(download_frame, text="Download", font=("Arial", 12, 'bold'),
                                fg="#FAF8F9", bg='#6677B8', activebackground="#808ec6", activeforeground="#FAF8F9",
                                cursor="hand2", command=self.save_all, padx=20, pady=10, width=5)
        save_button.pack(side='right', padx=(0, 60), pady=5)

        download_frame.pack(side='top', pady=20)

        separator = tk.Frame(self._frame, bg='#6677B8', height=3)
        separator.pack(fill=tk.X, side=tk.TOP, anchor="center")

    def save_all(self):
        """
        Saves the linear regression model along with its optional description.

        This method retrieves the description from the text area, validates it,
        and attempts to save the model. It shows appropriate message boxes for
        success or failure cases.

        Raises:
            Displays an error message box if the save operation fails
        """
        description = self._comment.get("1.0", "end-1c")

        # Check if the comment is empty
        if not description:
            # Show warning message
            messagebox.showwarning(
                "Warning", "The model does not include a description.")
            description = None

        try:
            extension = save_model(self._linear_regression, description)
            messagebox.showinfo(
                "Success", f"File saved as {extension} correctly.")
        except Exception as e:
            messagebox.showerror("Error", f"Fail to save the file: {str(e)}")

    def predict(self):
        entry_value = self._prediction_frame.get()
        print(f"Raw entry_value: '{entry_value}'")  # Para ver qué estás obteniendo exactamente
        target = self._linear_regression.target_name
        
        if not entry_value:
            # Show warning message
            messagebox.showwarning("Warning", "No value has been designated")
            entry_value = None
        
        else:
            try:
                number = float(entry_value)  # Convertir a float
                print(f"Converted number: {number}")  # Verificar que la conversión sea correcta
                prediction = self._linear_regression.make_prediction(number)
                
                messagebox.showinfo("", f"The predicted value of {target} for this entry is {prediction}")
            
            except ValueError:
                messagebox.showerror("Error", "Please enter a numeric value")


        



# Example of direct use of LinearRegressionInterface in a Tkinter window
if __name__ == "__main__":
    import pandas as pd

    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Linear regression interface")

    # Sample data for testing
    df = pd.DataFrame({
        "Feature": [2, 5, 0, 2, 1, 9, 8],
        "Target": [1, 3, 5, 5, 5, 1, 3]
    })

    # Create a frame in the main window for the linear regression interface
    frame = tk.Frame(root)
    frame.pack()

    # Create the linear regression interface
    app = LinearRegressionInterface(frame, df["Feature"], df["Target"])

    # Start the main tkinter loop
    root.mainloop()
