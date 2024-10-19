import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scr'))) # Esto hace que se pueda importar de otra carpeta
from open_files import open_file
import statsmodels.api as sm

route = str(input('Introduce la ruta absoluta del archivo (sin las comillas): '))
data = open_file(route)

print('Tabla leída')
print(data)

tipo = input('Quieres hacer regresión simple (S) o múltiple (M)? :')
if tipo == 'S' or tipo == 's':
    x_input = str(input('Introduce la columna de las x : '))
    x = data[[x_input]] # Importantes los dobles [[]] para que sea de dimensión 2 !
elif tipo == 'M' or tipo == 'm':
    x_input = []
    veces = int(input('Cuantas variables quieres poner en la columna de las x? :'))
    for vez in range(1,veces+1):
            num = str(input(f'Introduce la columna nº {vez} : '))
            x_input.append(num)
    x = data[x_input]

y_input = str(input('Introduce la columna de las y : '))
y = data[y_input]

modelo = sm.OLS(y,x)

modelofin = modelo.fit()

print(modelofin.summary())
