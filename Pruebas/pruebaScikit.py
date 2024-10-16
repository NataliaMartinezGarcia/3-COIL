import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

#  El reshape convierte la entrada en una matriz (si no no lo acepta el .fit). Para hacer el reshape tiene que ser un array.
X = np.array([2, 7, 30, 1, 45, 2, 9, 90]).reshape(-1, 1)  # Matriz de 1 columna (el segundo 1 indica el nº de columnas)
Y = [5, 10, 50, 3, 70, 6, 0, 5]  # La salida no necesita ser una matriz (puede serlo si se devuelve más de 1 valor)

# Crear el modelo de regresión lineal
modelo = LinearRegression()

# Ajustar el modelo con los datos
modelo.fit(X, Y)

# Predecir valores con el modelo entrenado
y_pred = modelo.predict(X)

# Mostrar los coeficientes de la regresión
print(f"Pendiente (coeficiente): {modelo.coef_[0]}")
print(f"Intercepto: {modelo.intercept_}")

# Calcular el Error Cuadrático Medio (MSE) -> Cuanto más bajo el valor, mejor ajustado está.
mse = mean_squared_error(Y, y_pred)
print(f"Error Cuadrático Medio (MSE): {mse}")

# Calcular el Coeficiente de Determinación (R²) -> Va de 0 a 1. Cuanto más cerca de 1 , mejor ajustado.
r2 = r2_score(Y, y_pred)
print(f"Coeficiente de Determinación (R²): {r2}")

'''
# Visualizar los datos y la línea de regresión
plt.scatter(X, Y, color='blue', label='Datos reales') # Hace los puntos
plt.plot(X, y_pred, color='red', label='Línea de regresión') # Hace la recta
plt.xlabel("X")
plt.ylabel("y")
plt.legend()
plt.show()
'''