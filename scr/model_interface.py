import tkinter as tk
from tkinter import messagebox
# import gui

def show(frame,feature_name,target_name,intercept,slope,r_squared,mse,description):
    """
    Displays the linear regression model results in a tkinter frame with a styled interface.
    
    Creates a formatted display showing the predicted equation, coefficient of determination (R²),
    mean square error (MSE), and an optional description of the model.
    
    Args:
        frame (tk.Frame): The parent frame where the results will be displayed
        feature_name (str): Name of the independent variable (X)
        target_name (str): Name of the dependent variable (Y)
        intercept (float): Y-intercept of the regression line
        slope (float): Slope coefficient of the regression line
        r_squared (float): R-squared value of the model (coefficient of determination)
        mse (float): Mean Square Error of the model
        description (str, optional): Additional description or interpretation of the model

    """
    # Create a border effect
    info_labels_border = tk.Frame(frame, bg = '#6677B8')
    info_labels_border.pack(side = 'top', pady = (40,0))

    info_labels = tk.Frame(info_labels_border, bg = '#d0d7f2')
    info_labels.pack(fill = tk.BOTH, padx = 3, pady = 3)

    # Create labels for each value and display them
    equation_frame = tk.Frame(info_labels, bg = '#d0d7f2')
    equation_frame.pack(side='top', fill='x', pady=5)

    equation_title = tk.Label(equation_frame, text="Predicted equation:", 
                            fg = '#4d598a', bg = '#d0d7f2', font=('Arial Black', 11,'bold'))
    equation_title.pack(side='left', padx=5)

    equation_label = tk.Label(equation_frame, text=f"{target_name} = {intercept:.2f} + {slope:.2f}*{feature_name}", 
                            fg = '#6677B8', bg = '#d0d7f2', font=('Arial Black', 11,'bold'))
    equation_label.pack(side='right', padx=5)

    # Pair 2: Coefficient of determination (R²)
    rsquared_frame = tk.Frame(info_labels, bg = '#d0d7f2')
    rsquared_frame.pack(side='top', fill='x', pady=5)

    rsquared_title = tk.Label(rsquared_frame, text="Coefficient of determination (R²):", 
                            fg = '#4d598a', bg = '#d0d7f2', font=('Arial Black', 11,'bold'))
    rsquared_title.pack(side='left', padx=5)

    rsquared_label = tk.Label(rsquared_frame, text=f"{r_squared:.4f}", 
                            fg = '#6677B8', bg = '#d0d7f2', font=('Arial Black', 11,'bold'))
    rsquared_label.pack(side='right', padx=5)

    # Pair 3: Mean Square Error (MSE)
    mse_frame = tk.Frame(info_labels, bg = '#d0d7f2')
    mse_frame.pack(side='top', fill='x', pady=5)

    mse_title = tk.Label(mse_frame, text="Mean Square Error (MSE):", 
                        fg = '#4d598a', bg = '#d0d7f2', font=('Arial Black', 11,'bold'))
    mse_title.pack(side='left', padx=5)

    mse_label = tk.Label(mse_frame, text=f"{mse:.4f}", 
                        fg = '#6677B8', bg = '#d0d7f2', font=('Arial Black', 11,'bold'))
    mse_label.pack(side='right', padx=5)

    # If description exists (not None or empty), display it in a label
    if description and description.strip():

        description_frame = tk.Frame(info_labels, bg = '#d0d7f2')
        description_frame.pack(side='top', fill='x', pady=5)

        description_title = tk.Label(description_frame, text="Description:", 
                                    fg = '#4d598a', bg = '#d0d7f2', font=('Arial Black', 11,'bold'))
        description_title.pack(side='left', padx=5)

        description_label = tk.Label(description_frame, text=description, fg = '#6677B8', bg = '#d0d7f2',
                                    font=('Arial Black', 11,'bold'), width=55)  
        description_label.pack(side='right', padx=(10, 20), pady=5)

