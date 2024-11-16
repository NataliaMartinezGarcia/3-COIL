import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from linear_regression import LinearRegression
import statsmodels.api as sm
from model_handler import save_model
import model_interface

class LinearRegressionInterface:
    def __init__(self, frame, feature, target):
        self._frame = frame  # Frame principal de la interfaz
        self._feature = feature  # Se lo pasaremos a la clase que hace los calculos
        self._target = target
        self._comment = None

        # Crear el objeto de regresión lineal para cálculos y resultados
        self._linear_regression = LinearRegression(feature, target)

        # Crear y mostrar el gráfico en la interfaz
        self.create_plot()

    def create_plot(self):
        # Extraer los datos necesarios para la gráfica
        predictions = self._linear_regression.predictions

        # Crear la figura de matplotlib
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#d0d7f2')  # Cambia el color de fondo de toda la figura (azul claro)

        ax.scatter(self._feature, self._target, color='#808ec6', label='Data', s=10)  # Puntos de datos reales
        ax.plot(self._feature, predictions, color='#bc2716', label='Regression line', linewidth=2)  # Línea de regresión
        ax.set_xlabel(self._linear_regression._feature_name, fontsize=8)
        ax.set_ylabel(self._linear_regression._target_name, fontsize=8)
        ax.tick_params(axis='both', which='major', labelsize=8)  # Tamaño de los números en los ejes
        ax.legend(fontsize=8)

        # Integrar la figura dentro del frame de tkinter
        canvas = FigureCanvasTkAgg(fig, master=self._frame)
        canvas.get_tk_widget().config(bg = '#d0d7f2')
        canvas.draw()
        canvas.get_tk_widget().pack()
       
        model_interface.show(self._frame,self._linear_regression.feature_name,self._linear_regression.target_name,self._linear_regression.intercept,
                             self._linear_regression.slope,self._linear_regression.r_squared,
                             self._linear_regression.mse,None)

        self.comment()

    def comment(self):
        
        download_frame = tk.Frame(self._frame, height=250, bg = '#d0d7f2')

        entry_frame = tk.Frame(download_frame, width=250, height=250, bg = '#d0d7f2')

        label = tk.Label(entry_frame,text = 'Write a description for the model (optional)', fg = '#4d598a', bg = '#d0d7f2',
                        font= ("DejaVu Sans Mono", 11, 'bold'),width = 50)
        label.pack(side='top', fill='x', padx=(10, 20), pady=5)

        self._comment = tk.Text(entry_frame, width=30, height=5, font=("Arial", 10,'bold'), wrap="word")
        self._comment.pack(side='top', fill=tk.BOTH, padx=20, pady=5)

        entry_frame.pack(side = 'left', padx = 40, pady = 10)

        save_button = tk.Button(download_frame, text="Download", font=("Arial", 12,'bold'),
                                  fg="#FAF8F9", bg = '#6677B8' ,activebackground="#808ec6",activeforeground="#FAF8F9",
                                  cursor="hand2", command = self.save_all, padx=20, pady=10,width = 5)
        save_button.pack(side='right', padx=(0,60), pady=5) 

        download_frame.pack(side = 'top', pady = 20)

        separator = tk.Frame(self._frame, bg = '#6677B8', height = 3)
        separator.pack(fill = tk.X, side = tk.TOP, anchor = "center")

    def save_all(self):
        description = self._comment.get("1.0", "end-1c")

        # Verificar si el comentario está vacío
        if not description:
            # Mostrar un mensaje de advertencia
            messagebox.showwarning("Warning", "The model does not include a description.")
            description = None

        try:
            extension = save_model(self._linear_regression, description)
            messagebox.showinfo("Success", f"File saved as {extension} correctly.")
        except Exception as e:
            messagebox.showerror("Error", f"Fail to save the file: {str(e)}")


# Ejemplo de uso directo de LinearRegressionInterface en una ventana Tkinter
if __name__ == "__main__":
    import pandas as pd

    # Crear la ventana principal de Tkinter
    root = tk.Tk()
    root.title("Linear regression interface")

    # Datos de ejemplo para pruebas directas
    df = pd.DataFrame({
        "Feature": [2, 5, 0, 2, 1, 9, 8],
        "Target": [1, 3, 5, 5, 5, 1, 3]
    })

    # Crear un frame en la ventana principal para la interfaz de regresión lineal
    frame = tk.Frame(root)
    frame.pack()

    # Crear la interfaz de regresión lineal
    app = LinearRegressionInterface(frame, df["Feature"], df["Target"])

    # Iniciar el loop principal de tkinter
    root.mainloop()