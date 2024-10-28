import pandas as pd
from tkinter import messagebox

class NaNHandler:
    """Clase para manejar la verificación y gestión de valores NaN en un DataFrame."""

    def __init__(self, df, method_names, selected_columns):
        self._df = df
        self._method_names = method_names  # Agregar el atributo method_names
        self._selected_columns = list(set(selected_columns))

        # DataFrame sobre el que se opera para no modificar el dado
        self._df_copy = self._df[self._selected_columns].copy()

    def check_for_nan(self):
        """Verifica si hay valores NaN en las columnas seleccionadas.

        Returns
        -------
        tuple
            Un booleano que indica si hay datos faltantes y un mensaje informativo.
        """
        missing_info = self._df[self._selected_columns].isnull().sum()
        missing_columns = missing_info[missing_info > 0]

        if not missing_columns.empty:
            nan_message = "Valores inexistentes detectados en las siguientes columnas:\n"
            for col, count in missing_columns.items():
                nan_message += f"- {col}: {count} valores faltantes\n"
            return True, nan_message
        else:
            return False, "No se detectaron valores inexistentes."

    def remove_rows(self, columns):
        """Elimina las filas con datos inexistentes en el DataFrame.

        Parámetros 
        ----------
        columns: list
            Lista de columnas en las que se eliminarán filas con NaN.

        Returns
        -------
        DataFrame
            DataFrame sin las filas que contenían NaN en las columnas especificadas.
        """
        return self._df_copy.dropna(subset=columns).copy()

    def fill_mean(self, columns):
        """Sustituye los datos inexistentes en cada columna del DataFrame
        por la media en esa columna.

        Parámetros 
        ----------
        columns: list
            Lista de columnas en las que se rellenarán NaN con la media.

        Returns
        -------
        DataFrame
            DataFrame con NaN rellenados con la media.
        """
        return self._df_copy.fillna(self._df_copy.mean())

    def fill_median(self, columns):
        """Sustituye los datos inexistentes en cada columna del DataFrame
        por la mediana en esa columna.

        Parámetros 
        ----------
        columns: list
            Lista de columnas en las que se rellenarán NaN con la mediana.

        Returns
        -------
        DataFrame
            DataFrame con NaN rellenados con la mediana.
        """
        return self._df_copy.fillna(self._df_copy.median())

    def fill_constant(self, columns, constant_value):
        """Sustituye los datos inexistentes en el DataFrame
        en cada columna por una constante 'constant_value'.

        Parámetros 
        ----------
        columns: list
            Lista de columnas en las que se rellenarán NaN con un valor constante.

        constant_value: float
            Valor constante con el que se rellenarán los NaN.

        Returns
        -------
        DataFrame
            DataFrame con NaN rellenados con el valor constante.
        """
        return self._df_copy.fillna(constant_value)

    def preprocess(self, method, constant_value=None):
        """Devuelve una copia preprocesada de las columnas 'columns'
        del DataFrame como indique 'method'.

        Precondiciones: 
        - 'columns' tiene que ser una lista con columnas válidas de 'df'.
        - Si 'method' = Rellenar con Valor Constante, 'constant_value' no puede ser None.

        Parámetros 
        ----------
        columns: list
            Columnas de 'df' a procesar.

        method: string
            Método de preprocesado.
            Posibles valores: 
            -"Eliminar Filas"
            -"Rellenar con Media"
            -"Rellenar con Mediana"
            -"Rellenar con Valor Constante"

        constant_value: float, optional
            Valor constante para rellenar los NaN, si corresponde al método.

        Returns
        -------
        DataFrame
            Copia de las columnas del DataFrame preprocesadas.
        """
        
        # Métodos y las funciones que les corresponden
        METHOD_FUNCTIONS = {
            "Eliminar Filas": self.remove_rows,
            "Rellenar con Media": self.fill_mean,
            "Rellenar con Mediana": self.fill_median,
            "Rellenar con Valor Constante": self.fill_constant,
        }

        # Comprobamos el método y llamamos a la función correspondiente
        if method == "Rellenar con Valor Constante":
            if constant_value is not None:
                return METHOD_FUNCTIONS[method](self._selected_columns, constant_value)
            else:
                messagebox.showerror("Error", "Debes introducir un valor numérico válido.")
                return None
        else:
            return METHOD_FUNCTIONS[method](self._selected_columns)

if __name__ == "__main__":
    # Ejemplo de uso del módulo
    import pandas as pd

    METHOD_NAMES = ("Eliminar Filas", "Rellenar con Media", 
               "Rellenar con Mediana", "Rellenar con Valor Constante")
    
    data = {
        "Columna1": [1, 2, None, 4],
        "Columna2": [None, 1, 2, 3],
        "Columna3": [1, None, None, 4],
        "Columna4": [5, 6, 7, 8],
    }
    df = pd.DataFrame(data)

    print("df Antes del preprocesado")
    print(df)

    nan = NaNHandler(df, METHOD_NAMES, ["Columna1", "Columna2", "Columna3"])
    has_missing, message = nan.check_for_nan()
    print(message)

    new_df = nan.preprocess("Rellenar con Media")

    print("\nnew_df después del preprocesado")
    print(new_df)

    print("\ndf después del preprocesado")
    print(df)