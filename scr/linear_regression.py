# linear_regression.py
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk

class LinearRegression:
    def __init__(self, feature, target):
        # Guardar las series de datos de las columnas seleccionadas
        self._feature_name = feature.name
        self._feature = feature
 
        self._target_name = target.name
        self._target = target

        self._predictions = None
        self._intercept = None
        self._slope = None
        self._r_squared = None
        self._mse = None

        self.create_regression(self._feature, self._target)
    
    @property
    def feature_name(self):
        return self._feature_name

    @property
    def target_name(self):
        return self._target_name

    @property 
    def predictions(self):
        return self._predictions

    @property
    def intercept(self):
        return self._intercept

    @property
    def slope(self):
        return self._slope

    @property
    def r_squared(self):
        return self._r_squared

    @property
    def mse(self):
        return self._mse

    
    def create_regression(self, feature, target):
        # Agregar una columna de unos para el término independiente
        feature_with_intercept = sm.add_constant(feature)
       
        # Entrenar el modelo
        model_training = sm.OLS(target, feature_with_intercept)
        modelofin = model_training.fit()
 
        # Coeficiente del término independiente y de la pendiente
        self._intercept, self._slope = modelofin.params
        self._r_squared = modelofin.rsquared
       
        # Predicciones del modelo
        self._predictions = modelofin.predict(feature_with_intercept)
       
        # ECM
        self._mse = np.mean((np.array(target) - self._predictions) ** 2)