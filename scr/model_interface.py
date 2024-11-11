import tkinter as tk
from tkinter import messagebox
import gui

def show(frame,feature_name,target_name,intercept,slope,r_squared,mse,description):

    info_labels = tk.Frame(frame, bg = '#d0d7f2')
    # Crear etiquetas para cada valor y mostrarlos
    equation_label = tk.Label(info_labels, text=f"Ecuación de la recta predicha: {target_name} = {intercept:.2f} + {slope:.2f}*{feature_name}",
                                fg="#FAF8F9", bg="#6677B8", font=("DejaVu Sans Mono", 11))
    equation_label.pack(side='top', pady=10, anchor='center')

    rsquared_label = tk.Label(info_labels, text=f"Coeficiente de determinación (R²): {r_squared:.4f}",
                                fg="#FAF8F9", bg="#6677B8", font=("DejaVu Sans Mono", 11))
    rsquared_label.pack(side='top', pady=10, anchor='center')

    mse_label = tk.Label(info_labels, text=f"Error Cuadrático Medio (ECM): {mse:.4f}", fg="#FAF8F9", bg="#6677B8",
                                font=("DejaVu Sans Mono", 11))
    mse_label.pack(side='top', padx=(10, 20), pady=5, anchor='center')

    # Si la descripción existe (no es None o vacía), mostrarla en una etiqueta
    if description and description.strip():

        description_label = tk.Label(info_labels, text=description, fg="#FAF8F9", bg="#6677B8",
                                        font=("DejaVu Sans Mono", 11), width=55)
        description_label.pack(side='top', padx=(10, 20), pady=5, anchor='w')

    info_labels.pack(side = 'top',fill = tk.X, anchor = 'center', pady = 20)
