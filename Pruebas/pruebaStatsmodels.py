import statsmodels.api as sm

X = [2, 7, 30, 1, 45, 2, 9, 90]
Y = [5, 10, 50, 3, 70, 6, 0, 5]

X = sm.add_constant(X)  # Esto añade una columna de 1 para que se pueda incluir el término independiente (intercepto)

# Crear el modelo de regresión lineal en statsmodels
modelo = sm.OLS(Y, X)

# Ajustar el modelo con los datos de entrenamiento
modelo_entrenado = modelo.fit()

# Hacer predicciones sobre los mismos datos de entrenamiento
y_pred = modelo_entrenado.predict(X)

# Mostrar el resumen del modelo
print(modelo_entrenado.summary())

# Calcular el Coeficiente de Determinación (R²)
r2 = modelo_entrenado.rsquared
print(f"Coeficiente de Determinación (R²): {r2}")

# Esta librería no tiene el mse como función !!!
