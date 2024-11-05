import pandas as pd
import joblib
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, filedialog, Frame, ttk, Text
import statsmodels.api as sm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SimpleRegressionApp:
    def __init__(self, master):
        self.master = master
        master.title("Modelo de Regresión Lineal Simple")
        master.geometry("600x700")

        # Crear un marco para los widgets
        self.frame = Frame(master)
        self.frame.pack(pady=20)

        # Etiqueta para mostrar mensajes al usuario
        self.message_label = Label(self.frame, text="", fg="blue")
        self.message_label.pack(pady=10)

        # Botón para cargar datos
        self.load_button = Button(self.frame, text="Cargar Datos CSV", command=self.load_data)
        self.load_button.pack(pady=5)

        # Combobox para seleccionar la columna de entrada
        self.input_combobox = ttk.Combobox(self.frame, width=47)
        self.input_combobox.pack(pady=5)

        # Combobox para seleccionar la columna de salida
        self.target_combobox = ttk.Combobox(self.frame, width=47)
        self.target_combobox.pack(pady=5)

        # Área de texto para la descripción del modelo
        self.description_label = Label(self.frame, text="Descripción del Modelo (opcional):")
        self.description_label.pack(pady=5)

        self.description_text = Text(self.frame, height=5, width=50)
        self.description_text.pack(pady=5)

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
        self.data = None
        
        self.model = None
        self.feature_column = None  # Para almacenar la columna de entrada
        self.target_column = None    # Para almacenar la columna de salida
        self.description = ""         # Almacenar la descripción del modelo

        # Canvas para la gráfica
        self.canvas = None
        self.formula_label = Label(self.frame, text="", fg="green")
        self.formula_label.pack(pady=10)  # Para mostrar la fórmula

        # Etiqueta para mostrar la descripción del modelo
        self.loaded_description_label = Label(self.frame, text="", fg="black")
        self.loaded_description_label.pack(pady=10)

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                self.input_combobox['values'] = self.data.columns.tolist()  # Cargar columnas en el combobox de entrada
                self.target_combobox['values'] = self.data.columns.tolist()  # Cargar columnas en el combobox de salida
                self.update_message("Datos cargados exitosamente.")
            except Exception as e:
                self.update_message(f"Error al cargar el archivo: {e}")

    def train_model(self):
        if self.data is not None:
            self.feature_column = self.input_combobox.get()  # Obtener la columna seleccionada para X
            self.target_column = self.target_combobox.get()    # Obtener columna objetivo y

            if self.feature_column and self.target_column:  # Comprobamos que haya columnas seleccionadas
                X = self.data[[self.feature_column]]
                y = self.data[self.target_column]

                # Agregamos constante para la regresión
                X = sm.add_constant(X)

                # Crear y ajustar el modelo
                self.model = sm.OLS(y, X).fit()     # Entrenar
                self.description = self.description_text.get("1.0", "end-1c").strip()  # Obtener descripción
                self.update_message("Modelo entrenado exitosamente.")
                self.show_formula()  # Mostrar fórmula después de entrenar el modelo
            else:
                self.update_message("Selecciona una columna de entrada y una columna de salida.")
        else:
            self.update_message("Carga datos antes de entrenar el modelo.")

    def show_formula(self):
    # Mostrar la fórmula del modelo
        params = self.model.params
        formula = f"{self.target_column} = {params.iloc[0]:.4f} + {params.iloc[1]:.4f} * {self.feature_column}" # Uso iloc porque si no me informaba de un error para las futuras versiones de pandas
        self.formula_label.config(text=f"Fórmula del modelo ==>  {formula}")


    def save_model(self):
        if self.model is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
            if file_path:
                # Guardar el modelo y las columnas de entrada/salida junto con la descripción
                joblib.dump((self.model, self.feature_column, self.target_column, self.description), file_path)
                self.update_message("Modelo y datos guardados exitosamente.")
        else:
            self.update_message("No hay modelo para guardar.")

    def load_model(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl")])
        if file_path:
            loaded = joblib.load(file_path) # Método para cargar el modelo 
            self.model = loaded[0]
            self.feature_column = loaded[1]
            self.target_column = loaded[2]
            self.description = loaded[3]  # Cargar la descripción
            self.description_text.delete("1.0", "end")  # Limpiar el área de texto
            self.description_text.insert("1.0", self.description)  # Mostrar la descripción
            self.loaded_description_label.config(text=self.description)  # Mostrar la descripción en la etiqueta
            self.update_message("Modelo cargado exitosamente.")
            self.show_formula()  # Mostrar la fórmula cargada
            self.plot_model()  # Mostrar la gráfica después de cargar el modelo

    def plot_model(self):
        if self.model is not None and self.feature_column and self.target_column:
            X = self.data[[self.feature_column]]
            y = self.data[self.target_column]

            # Agregar constante para la regresión
            X = sm.add_constant(X)

            # Realizar predicciones
            predictions = self.model.predict(X)

            # Crear la figura de la gráfica
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.scatter(X[self.feature_column], y, label='Valores Reales', alpha=0.6)
            ax.plot(X[self.feature_column], predictions, color='red', label='Línea de Regresión', linestyle='--')
            ax.set_xlabel(f"Entrada {self.feature_column}")
            ax.set_ylabel(f"Objetivo ({self.target_column})")
            ax.set_title("Predicciones vs. Valores Reales")
            ax.legend()
            ax.grid()

            # Si ya hay un canvas, lo eliminamos antes de crear uno nuevo
            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            # Crear un nuevo canvas para la gráfica
            self.canvas = FigureCanvasTkAgg(fig, master=self.frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(pady=20)  # Agregar el canvas a la interfaz

        else:
            self.update_message("No hay datos o modelo para graficar.")

    def update_message(self, message):
        self.message_label.config(text=message)

if __name__ == "__main__":
    root = Tk()  # Crear la ventana principal
    app = SimpleRegressionApp(root)  # Inicializar la aplicación
    root.mainloop()  # Ejecutar el bucle principal de la interfaz gráfica




