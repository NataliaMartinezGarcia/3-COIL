# linear_regression.py
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
 
class LinearRegression:
    def __init__(self, feature, target, output_labels):
        # Guardar las series de datos de las columnas seleccionadas
        self._feature_name = feature.name
        self._feature = feature
 
        self._target_name = target.name
        self._target = target
 
        self.output_labels = output_labels  # Almacenar los labels para mostrar los resultados
        self.create_regression(self._feature, self._target)
       
    def create_regression(self, feature, target):
        # Agregar una columna de unos para el término independiente
        feature_with_intercept = sm.add_constant(feature)
       
        # Entrenar el modelo
        model_training = sm.OLS(target, feature_with_intercept)
        self.modelofin = model_training.fit()
 
        # Coeficiente del término independiente y de la pendiente
        intercept, slope = self.modelofin.params
        r_squared = self.modelofin.rsquared
       
        # Predicciones del modelo
        predictions = self.modelofin.predict(feature_with_intercept)
       
        # ECM
        mse = np.mean((np.array(target) - predictions) ** 2)
 
        # Actualizar etiquetas con los resultados
        self.output_labels[0].config(text=f"Ecuación de la recta predicha: {self._target_name} = {intercept:.2f} + {slope:.2f}*{self._feature_name}")
        self.output_labels[1].config(text=f"Coeficiente de determinación (R²): {r_squared:.4f}")
        self.output_labels[2].config(text=f"Error Cuadrático Medio (ECM): {mse:.4f}")
 
        # Visualizar los datos y la línea de regresión
        plt.scatter(feature, target, color='blue', label='Datos reales')  # Hace los puntos
        plt.plot(feature, predictions, color='red', label='Línea de regresión')  # Hace la recta
        plt.xlabel(self._feature_name)
        plt.ylabel(self._target_name)
        plt.legend()
        plt.show()
 
# Solo si se ejecuta directamente este archivo
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Modelo de Regresión Lineal")
 
    # Datos de ejemplo para pruebas directas del archivo
    df = pd.DataFrame({
        "Feature": [2, 5, 0, 2, 1, 9, 8],
        "Target": [1, 3, 5, 5, 5, 1, 3]
    })
 
    # Crear etiquetas para mostrar resultados
    output_labels = []
    for i in range(3):
        label = tk.Label(root, text="", wraplength=400)
        label.pack(pady=5)
        output_labels.append(label)
 
    # Prueba directa con datos de ejemplo
    LinearRegression(df["Feature"], df["Target"], output_labels)
 
    root.mainloop()