# Este es un archivo de prueba para guardar, cargar, hacer predicciones y visualizar los modelos de regresión lineal
# Como no tiene implementado el preprocesamiento, falla si hay valores nan, pero ya tenemos eso soluconado en el main

import pandas as pd
import joblib
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, filedialog, Frame, Listbox, MULTIPLE, ttk
from sklearn.linear_model import LinearRegression

# Se crea una ventana de tkinter simplemente para tener un menú para hacer las pruebas
class SimpleRegressionApp:
    def __init__(self, master):
        self.master = master
        master.title("Modelo de Regresión Lineal")
        master.geometry("500x400")

        # Se crea un marco para los widgets
        self.frame = Frame(master)
        self.frame.pack(pady=20)

        # Etiqueta para mostrar mensajes al usuario
        self.message_label = Label(self.frame, text="", fg="blue")
        self.message_label.pack(pady=10)

        # Botón para cargar datos
        self.load_button = Button(self.frame, text="Cargar Datos CSV", command=self.load_data)
        self.load_button.pack(pady=5)

        # Listbox para seleccionar las columnas de entrada
        self.input_listbox = Listbox(self.frame, selectmode=MULTIPLE, width=50, height=5)
        self.input_listbox.pack(pady=5)

        # Combobox para seleccionar la columna de salida
        self.target_combobox = ttk.Combobox(self.frame, width=47)
        self.target_combobox.pack(pady=5)

        # Botón para entrenar el modelo
        self.train_button = Button(self.frame, text="Entrenar Modelo", command=self.train_model)
        self.train_button.pack(pady=5)

        # Botón para guardar el modelo
        self.save_button = Button(self.frame, text="Guardar Modelo", command=self.save_model)
        self.save_button.pack(pady=5)

        # Botón para cargar un modelo
        self.load_model_button = Button(self.frame, text="Cargar Modelo", command=self.load_model)
        self.load_model_button.pack(pady=5)

        # Inicializar variables
        self.model = None
        self.data = None
        self.saved_data = None  # Para almacenar los datos del modelo guardado
        self.feature_columns = None  # Para almacenar las columnas usadas para entrenar

    # El cargar datos del main ya tiene la funcionalidad completa, este es de prueba
    def load_data(self):
        # Cargar un archivo CSV y llenar Listbox y Combobox
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            self.input_listbox.delete(0, 'end')
            for col in self.data.columns:
                self.input_listbox.insert('end', col)
            self.target_combobox['values'] = self.data.columns.tolist()
            self.update_message("Datos cargados exitosamente.")

    def train_model(self):
        if self.data is not None:
            selected_columns = self.input_listbox.curselection()  # Obtener columnas seleccionadas para x
            target_column = self.target_combobox.get()  # Obtener columna objetivo y

            if selected_columns and target_column:   # Comprobamos que haya columnas seleccionadas
                X_columns = [self.data.columns[i] for i in selected_columns]
                X = self.data[X_columns]
                y = self.data[target_column]
                self.model = LinearRegression()  # Crear el modelo de regresión
                self.model.fit(X, y)  # Entrenar el modelo, el método ya viene creado en la librería y es necesario para poder obtener las predicciones.
                self.saved_data = self.data[X_columns + [target_column]]  # Almacenar los datos usados porque si no los archivos 
                # guardados no podrían ser cargados sin depender de las columnas seleccionadas en el momento, lo cuál no es lo que queremos
                self.feature_columns = X_columns  # Almacenar las columnas de características, necesario para que se cargue bien el archivo
                self.update_message("Modelo entrenado exitosamente.")
            else:
                self.update_message("Selecciona columnas de entrada y una columna de salida.")
        else:
            self.update_message("Carga datos antes de entrenar el modelo.")

    def save_model(self):
        if self.model is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")]) # Elegimos donde guardar el archivo
            if file_path:
                #. dump sirve para guardar un modelo
                joblib.dump((self.model, self.saved_data, self.feature_columns), file_path)  # Guardo todos los datos comentados antes para poder cargarlo en un futuro
                self.update_message("Modelo y datos guardados exitosamente.")
        else:
            self.update_message("No hay modelo para guardar.")

    def load_model(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl")])
        if file_path:
            loaded = joblib.load(file_path)  # Cargar el modelo y los datos
            self.model = loaded[0] # Modelo en si
            self.saved_data = loaded[1] # Datos de las columnas
            self.feature_columns = loaded[2]  # Cargar las columnas utilizadas
            self.update_message("Modelo cargado exitosamente.")
            self.plot_model()  # Mostrar la gráfica del modelo

    # Queda más claro el experimento viendo los modelos gráficamente para verificar si se han cargado bien.
    def plot_model(self):
        if self.saved_data is not None and self.model is not None:
            target_column = self.saved_data.columns[-1]  # Última columna como target
            X = self.saved_data[self.feature_columns]
            y = self.saved_data[target_column]

            # Realizar predicciones
            predictions = self.model.predict(X)

            # Graficar
            plt.figure(figsize=(10, 6))

            for i, col in enumerate(self.feature_columns):
                plt.scatter(X[col], y, label=f'Valores Reales de {col}', alpha=0.6)

                # Añadir línea de regresión
                plt.plot(X[col], predictions, linestyle='--', label=f'Línea de Regresión para {col}')

            plt.xlabel("Valores de Entrada")
            plt.ylabel(f"Objetivo ({target_column})")
            plt.title("Predicciones vs. Valores Reales")
            plt.legend()  # Mostrar la leyenda
            plt.grid()
            plt.show()  # Mostrar la gráfica
        else:
            self.update_message("No hay datos o modelo para graficar.")


    def update_message(self, message):
        # Método para actualizar el mensaje mostrado al usuario
        self.message_label.config(text=message)

if __name__ == "__main__":
    root = Tk()  # Crear la ventana principal
    app = SimpleRegressionApp(root)  # Inicializar la aplicación
    root.mainloop()  # Ejecutar el bucle principal de la interfaz gráfica

















