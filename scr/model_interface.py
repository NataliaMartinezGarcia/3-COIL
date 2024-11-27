import tkinter as tk
from tkinter import messagebox


def show(frame, feature_name, target_name, intercept, slope, r_squared, mse, description):
    show_info(frame, feature_name, target_name, intercept,
              slope, r_squared, mse, description)
    show_predictions(frame, intercept, slope, target_name, feature_name)


def show_info(frame, feature_name, target_name, intercept, slope, r_squared, mse, description):
    """
    Displays the linear regression model results in a tkinter frame with a styled interface.

    Creates a formatted display showing the predicted equation, coefficient of determination (R²),
    mean square error (MSE), and an optional description of the model.

    Attributes:
        - frame (tk.Frame): The parent frame where the results will be displayed
        - feature_name (str): Name of the independent variable (X)
        - target_name (str): Name of the dependent variable (Y)
        - intercept (float): Y-intercept of the regression line
        - slope (float): Slope coefficient of the regression line
        - r_squared (float): R-squared value of the model (coefficient of determination)
        - mse (float): Mean Square Error of the model
        - description (str, optional): Additional description or interpretation of the model
    """

    # Create a border effect
    info_labels_border = tk.Frame(frame, bg='#6677B8')
    info_labels_border.pack(side='top', pady=(40, 0))

    info_labels = tk.Frame(info_labels_border, bg='#d0d7f2')
    info_labels.pack(fill=tk.BOTH, padx=3, pady=3)

    # Create labels for each value and display them
    equation_frame = tk.Frame(info_labels, bg='#d0d7f2')
    equation_frame.pack(side='top', fill='x', pady=5)

    equation_title = tk.Label(equation_frame, text="Predicted equation:",
                              fg='#4d598a', bg='#d0d7f2', font=('Arial Black', 11, 'bold'))
    equation_title.pack(side='left', padx=5)

    equation_label = tk.Label(equation_frame, text=f"{target_name} = {intercept:.2f} + {slope:.2f}*{feature_name}",
                              fg='#6677B8', bg='#d0d7f2', font=('Arial Black', 11, 'bold'))
    equation_label.pack(side='right', padx=5)

    # Pair 2: Coefficient of determination (R²)
    rsquared_frame = tk.Frame(info_labels, bg='#d0d7f2')
    rsquared_frame.pack(side='top', fill='x', pady=5)

    rsquared_title = tk.Label(rsquared_frame, text="Coefficient of determination (R²):",
                              fg='#4d598a', bg='#d0d7f2', font=('Arial Black', 11, 'bold'))
    rsquared_title.pack(side='left', padx=5)

    rsquared_label = tk.Label(rsquared_frame, text=f"{r_squared:.4f}",
                              fg='#6677B8', bg='#d0d7f2', font=('Arial Black', 11, 'bold'))
    rsquared_label.pack(side='right', padx=5)

    # Pair 3: Mean Square Error (MSE)
    mse_frame = tk.Frame(info_labels, bg='#d0d7f2')
    mse_frame.pack(side='top', fill='x', pady=5)

    mse_title = tk.Label(mse_frame, text="Mean Square Error (MSE):",
                         fg='#4d598a', bg='#d0d7f2', font=('Arial Black', 11, 'bold'))
    mse_title.pack(side='left', padx=5)

    mse_label = tk.Label(mse_frame, text=f"{mse:.4f}",
                         fg='#6677B8', bg='#d0d7f2', font=('Arial Black', 11, 'bold'))
    mse_label.pack(side='right', padx=5)

    # If description exists (not None or empty), display it in a label
    if description and description.strip():

        description_frame = tk.Frame(info_labels, bg='#d0d7f2')
        description_frame.pack(side='top', fill='x', pady=5)

        description_title = tk.Label(description_frame, text="Description:",
                                     fg='#4d598a', bg='#d0d7f2', font=('Arial Black', 11, 'bold'))
        description_title.pack(side='left', padx=5)

        description_label = tk.Label(description_frame, text=description, fg='#6677B8', bg='#d0d7f2',
                                     font=('Arial Black', 11, 'bold'))
        description_label.pack(side='right', padx=(10, 20), pady=5)


def show_predictions(frame, intercept, slope, target_name, feature_name):
    """
    Creates and displays the prediction interface for the linear regression model.

    Sets up an interactive interface allowing users to input feature values and 
    get predicted target values based on the regression model.

    Parameters:
        - frame (tk.Frame): The parent frame for the prediction interface
        - intercept (float): Y-intercept of the regression line
        - slope (float): Slope coefficient of the regression line
        - target_name (str): Name of the dependent variable
        - feature_name (str): Name of the independent variable
    """
    # Entry and button for user input to make predictions
    def make_prediction():
        """
        Calculates and displays the predicted value based on user input.

        Retrieves the user-input feature value, calculates the predicted target value
        using the regression equation, and displays the result. Shows an error message
        if the input is not a valid number.

        Raises:
            - ValueError: If the user input cannot be converted to a float
        """
        try:
            # Get the value entered by the user for the feature (X)
            feature_value = float(entry.get())
            # Calculate the predicted target value (Y) using the linear regression formula
            predicted_value = intercept + slope * feature_value
            result_label.config(
                text=f"Predicted {target_name}: {predicted_value:.2f}")
            result_label.pack(side='top', pady=(0, 20))

        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Please enter a valid numeric value for the feature.")

    # Frame for user input
    predictions_border = tk.Frame(frame, bg='#6677B8')
    predictions_border.pack(side='top', pady=40)

    predictions_labels = tk.Frame(predictions_border, bg='#d0d7f2')
    predictions_labels.pack(fill=tk.BOTH, padx=3, pady=3)

    title = tk.Label(predictions_labels, text='PREDICT A VALUE', fg='#4d598a', bg='#d0d7f2',
                     font=('Arial Black', 12, 'bold'))
    title.pack(side='top', pady=10)

    input_frame = tk.Frame(predictions_labels, bg='#d0d7f2')
    input_frame.pack(side='top', pady=(0, 20), padx=5)

    input_label = tk.Label(input_frame, text=f"Enter {feature_name} value:", fg='#4d598a', bg='#d0d7f2',
                           font=('Arial Black', 11, 'bold'))
    input_label.pack(side='left', padx=5)

    entry = tk.Entry(input_frame, font=('Arial', 12), width=5)
    entry.pack(side='left', padx=5)

    # Button to make the prediction
    predict_button = tk.Button(input_frame, text="Predict", command=make_prediction, font=('Arial Black', 10),
                               fg="#FAF8F9", bg='#6677B8', activebackground="#808ec6", activeforeground="#FAF8F9",
                               cursor="hand2")
    predict_button.pack(side='left', padx=5)

    # Label to show the prediction result
    result_label = tk.Label(predictions_labels, text="", fg='#6677B8',
                            bg='#d0d7f2', font=('Arial Black', 11, 'bold'))
    result_label.pack_forget()
