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
 
        self._predictions = None

        self._output_labels = output_labels  # Almacenar los labels para mostrar los resultados
        self.create_regression(self._feature, self._target)
    
    @property 
    def predictions(self):
        return self._predictions
    
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
        self._predictions = self.modelofin.predict(feature_with_intercept)
       
        # ECM
        mse = np.mean((np.array(target) - self._predictions) ** 2)

        # Actualizar etiquetas con los resultados
        self._output_labels[0].config(text=f"Ecuación de la recta predicha: {self._target_name} = {intercept:.2f} + {slope:.2f}*{self._feature_name}")
        self._output_labels[1].config(text=f"Coeficiente de determinación (R²): {r_squared:.4f}")
        self._output_labels[2].config(text=f"Error Cuadrático Medio (ECM): {mse:.4f}")
