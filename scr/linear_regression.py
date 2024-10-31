import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class LinearRegression:
    def __init__(self,feature,target):
        # Guardar el nombre de las columnas
        self._feature_name = feature.columns[0]
        self._feature = feature[self._feature_name]

        self._target_name = target.columns[0]
        self._target = target[self._target_name]

        self._create_regression(self._feature,self._target)
        
    def _create_regression(self, feature, target):
        # Agregamos una columna de unos para el término independiente
        feature_with_intercept = sm.add_constant(feature)
        
        # Entrenamos el modelo
        model_training = sm.OLS(target, feature_with_intercept)
        self.modelofin = model_training.fit()

        # Coeficiente del término independiente y de la pendiente
        intercept, slope = self.modelofin.params
        r_squared = self.modelofin.rsquared
        
        # Predicciones del modelo
        predictions = self.modelofin.predict(feature_with_intercept)
        
        # ECM
        mse = np.mean((np.array(target) - predictions) ** 2)

        # Imprimimos todo
        print(f"Ecuación de la recta predicha: {self._target_name} = {intercept:.2f} + {slope:.2f}*{self._feature_name}")
        print(f"Coeficiente de determinación (R²): {r_squared:.4f}")
        print(f"Error Cuadrático Medio (ECM): {mse:.4f}")   

        # Visualizar los datos y la línea de regresión
        plt.scatter(feature, target, color='blue', label='Datos reales') # Hace los puntos
        plt.plot(feature, predictions, color='red', label='Línea de regresión') # Hace la recta
        plt.xlabel(self._feature_name)
        plt.ylabel(self._target_name)
        plt.legend()
        plt.show()


def main():
    df_feature = pd.DataFrame({"Hola": [2, 5, 0, 2, 1, 9, 8]})
    df_target = pd.DataFrame({"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA": [1, 3, 5, 5, 5, 1, 3]})

    # Llamada al modelo de regresión usando los DataFrames
    LinearRegression(df_feature, df_target)
if __name__ == "__main__":
    main()
