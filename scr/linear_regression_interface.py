"""import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from linear_regression import LinearRegression
import statsmodels.api as sm

class LinearRegressionInterface:
    def __init__(self, frame, feature, target):
        self._frame = frame  # Frame principal de la interfaz
        self.feature = feature
        self.target = target

        # Crear etiquetas para mostrar resultados
        self.output_labels = []
        for i in range(3):
            label = tk.Label(self._frame, text="", wraplength=400)
            label.pack(pady=5)
            self.output_labels.append(label)

        # Crear el objeto de regresión lineal para cálculos y resultados
        self.linear_regression = LinearRegression(feature, target, self.output_labels)

        # Crear y mostrar el gráfico en la interfaz
        self.create_plot()

    def create_plot(self):
        # Extraer los datos necesarios para la gráfica
        feature = self.feature
        target = self.target
        predictions = self.linear_regression.modelofin.predict(sm.add_constant(feature))

        # Crear la figura de matplotlib
        fig, ax = plt.subplots()
        ax.scatter(feature, target, color='blue', label='Datos reales')  # Puntos de datos reales
        ax.plot(feature, predictions, color='red', label='Línea de regresión')  # Línea de regresión
        ax.set_xlabel(self.linear_regression._feature_name)
        ax.set_ylabel(self.linear_regression._target_name)
        ax.legend()

        # Integrar la figura dentro del frame de tkinter
        canvas = FigureCanvasTkAgg(fig, master=self._frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

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
    root.mainloop()"""

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from linear_regression import LinearRegression
import statsmodels.api as sm

class LinearRegressionInterface:
    def __init__(self, frame, feature, target):
        self._frame = frame  # Frame principal de la interfaz
        self._feature = feature  # Se lo pasaremos a la clase que hace los calculos
        self._target = target

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