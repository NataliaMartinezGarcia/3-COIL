import tkinter as tk  
from tkinter import ttk
import pandas as pd
import numpy as np
 
# Clase para gestionar la tabla de datos con barras deslizables.
class ScrollTable(ttk.Treeview):

    def __init__(self, frame):
        super().__init__(frame, columns=[], show="headings")
        self._frame = frame
        self._data = None  # En el momento de crearla, la tabla está vacía
 
        # Crea tabla y scrollbars pero permanecen ocultas hasta que la tabla tenga datos
 
        # Barra de desplazamiento horizontal
        self._scroll_x = tk.Scrollbar(self._frame, orient=tk.HORIZONTAL)
 
        # Barra de desplazamiento vertical
        self._scroll_y = tk.Scrollbar(self._frame, orient=tk.VERTICAL)
 
        # Conectar las barras de desplazamiento a la tabla existente (self)
        self.config(xscrollcommand=self._scroll_x.set, yscrollcommand=self._scroll_y.set)
 
        # Configuramos las barras de desplazamiento
        self._scroll_x.config(command=self.xview)
        self._scroll_y.config(command=self.yview)
 
        # self._frame.pack_propagate(True)  # Evitar que el frame cambie de tamaño"""
 
    @property  # DataFrame que muestra la tabla
    def data(self):
        return self._data
    
    def empty_table(self):
        """Elimina todos los elementos de la tabla existente."""
        self.delete(*self.get_children())
 
    def create_from_df(self, df):
        """Configura las columnas de la tabla según el DataFrame proporcionado.
        Inserta datos en el Treeview desde ese DataFrame."""
        self._data = df
        self['columns'] = list(df.columns)
        for col in df.columns:
            self.heading(col, text=col)
            self.column(col, anchor='center')
        
        for _, row in df.iterrows():
            self.insert("", "end", values=list(row))
 
    def show(self):
        """Muestra la tabla y los scrollbars en el frame."""
        self._scroll_x.pack(side=tk.TOP, fill=tk.X)  # Barra horizontal en la parte superior
        self._scroll_y.pack(side=tk.LEFT, fill=tk.Y)  # Barra vertical a la derecha
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # Tabla
 
    def numeric_columns(self):
        """Devuelve nombres de las columnas con variables numéricas."""
        return self._data.select_dtypes(include=['number']).columns


# Código para probar la clase ScrollTable
if __name__ == "__main__":
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Demo de ScrollTable")
    root.geometry("300x400")

    # Crear un marco para la tabla
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Crear una instancia de ScrollTable
    table = ScrollTable(frame)

    # Crear datos de ejemplo en un DataFrame con muchas filas y columnas
    num_rows = 200  # Aumentar el número de filas
    num_columns = 10  # Aumentar el número de columnas
    data = {
        "ID": np.arange(1, num_rows + 1),
        "Nombre": [f"Nombre {i}" for i in range(1, num_rows + 1)],
        "Edad": np.random.randint(18, 60, size=num_rows),
        "Ciudad": [f"Ciudad {i}" for i in range(1, num_rows + 1)],
        "Salario": np.random.randint(20000, 100000, size=num_rows),
        "Departamento": [f"Dep {i}" for i in range(1, num_rows + 1)],
        "Email": [f"email{i}@ejemplo.com" for i in range(1, num_rows + 1)],
        "Teléfono": [f"555-{i:04d}" for i in range(1, num_rows + 1)],
        "Fecha de Ingreso": pd.date_range(start='2020-01-01', periods=num_rows, freq='D').tolist(),
        "Evaluación": np.random.randint(1, 6, size=num_rows)  # Evaluación de 1 a 5
    }
    
    df = pd.DataFrame(data)

    # Cargar datos en la tabla
    table.create_from_df(df)

    # Mostrar la tabla
    table.show()

    # Iniciar el bucle principal de la interfaz gráfica
    root.mainloop()