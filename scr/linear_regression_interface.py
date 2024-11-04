import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from linear_regression import LinearRegression
import statsmodels.api as sm

class LinearRegressionInterface:
    def __init__(self, frame, feature, target):
        self._frame = frame  # Frame principal de la interfaz
        self._feature = feature  # Se lo pasaremos a la clase que hace los calculos
        self._target = target
        self._comment = None

        # Crear etiquetas para mostrar los resultados de la regresión
        self._output_labels = []
        for i in range(3):
            label = tk.Label(self._frame, text="", wraplength=400)
            label.pack(pady=5)
            self._output_labels.append(label)

        # Crear el objeto de regresión lineal para cálculos y resultados
        self._linear_regression = LinearRegression(feature, target, self._output_labels)

        # Crear y mostrar el gráfico en la interfaz
        self.create_plot()

    def create_plot(self):
        # Extraer los datos necesarios para la gráfica
        predictions = self._linear_regression.predictions

        # Crear la figura de matplotlib
        fig, ax = plt.subplots()
        ax.scatter(self._feature, self._target, color='blue', label='Datos reales', s=10)  # Puntos de datos reales
        ax.plot(self._feature, predictions, color='red', label='Línea de regresión', linewidth=2)  # Línea de regresión
        ax.set_xlabel(self._linear_regression._feature_name, fontsize=8)
        ax.set_ylabel(self._linear_regression._target_name, fontsize=8)
        ax.tick_params(axis='both', which='major', labelsize=8)  # Tamaño de los números en los ejes
        ax.legend(fontsize=8)

        # Integrar la figura dentro del frame de tkinter
        canvas = FigureCanvasTkAgg(fig, master=self._frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
        self.comment()

    def comment(self):
        
        entry_frame = tk.Frame(self._frame, width=290, height=300)

        label = tk.Label(entry_frame,text = 'Introduce un comentario para el modelo (opcional)',  fg= "#FAF8F9", bg = '#6677B8',
                        font= ("DejaVu Sans Mono", 11),width = 50)
        label.pack(side='top', fill='x', padx=(10, 20), pady=5)

        self._comment = tk.Text(entry_frame, width=30, height=8, font=("Arial", 10,'bold'), wrap="word")
        self._comment.pack(side='top', fill=tk.BOTH, padx=20, pady=5)

        entry_frame.pack(side = 'left', pady = 10)

        save_button = tk.Button(self._frame, text="Descargar", font=("Arial", 12,'bold'),
                                  fg="#FAF8F9", bg = '#6677B8' ,activebackground="#808ec6",activeforeground="#FAF8F9",
                                  cursor="hand2", command = self.save_description, padx=20, pady=10,width = 5)
        save_button.pack(side='right', padx=20, pady=5) 

    def save_description(self):
        text = self._comment.get("1.0", "end-1c")

        # Verificar si el comentario está vacío
        if not text:
            # Mostrar un mensaje de advertencia
            messagebox.showwarning("Advertencia", "El modelo no incluye una descripción")
        else:
            messagebox.showwarning("Información", f"Descripción guardada: {text}")


# Ejemplo de uso directo de LinearRegressionInterface en una ventana Tkinter
if __name__ == "__main__":
    import pandas as pd

    # Crear la ventana principal de Tkinter
    root = tk.Tk()
    root.title("Interfaz de Regresión Lineal")

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