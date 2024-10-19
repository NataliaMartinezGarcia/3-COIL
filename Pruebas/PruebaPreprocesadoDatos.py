import tkinter as tk  
from tkinter import messagebox, filedialog, ttk  
import open_files  
import pandas as pd  

# Clase para gestionar la tabla de datos
class ScrollTable(ttk.Treeview):
    def __init__(self, frame):
        super().__init__(frame, columns=[], show="headings")  # Inicializa la tabla
        self._frame = frame  # Guarda la referencia al marco que contiene la tabla

        # Crea barras de desplazamiento horizontal y vertical
        self._scroll_x = tk.Scrollbar(self._frame, orient=tk.HORIZONTAL)
        self._scroll_y = tk.Scrollbar(self._frame, orient=tk.VERTICAL)

        # Configura las barras de desplazamiento con la tabla
        self.config(xscrollcommand=self._scroll_x.set, yscrollcommand=self._scroll_y.set)
        self._scroll_x.config(command=self.xview)  # Conecta la barra horizontal
        self._scroll_y.config(command=self.yview)   # Conecta la barra vertical
        self._frame.pack_propagate(False)  # Evita que el marco cambie de tamaño

    def empty_table(self):  
        """Limpia la tabla eliminando todas las filas."""
        self.delete(*self.get_children())  # Elimina todas las filas existentes

    def create_from_df(self, df):
        """Crea la tabla a partir de un DataFrame de pandas."""
        self['columns'] = list(df.columns)  # Establece las columnas de la tabla
        for col in df.columns:
            self.heading(col, text=col)  # Configura el encabezado de cada columna
            self.column(col, anchor='center')  # Centra el texto en las columnas
        
        for _, row in df.iterrows():
            self.insert("", "end", values=list(row))  # Inserta cada fila del DataFrame en la tabla

    def show(self):
        """Muestra las barras de desplazamiento y la tabla."""
        self._scroll_x.pack(side=tk.TOP, fill=tk.X)  # Coloca la barra horizontal en la parte superior
        self._scroll_y.pack(side=tk.RIGHT, fill=tk.Y)  # Coloca la barra vertical a la derecha
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)  # Empaqueta la tabla en el marco

# Clase principal para gestionar la interfaz gráfica
class DataExplorerApp:
    def __init__(self, ventana):
        self._ventana = ventana  # Guarda la ventana principal
        self._ventana.title("Data Explorer")  # Establece el título de la ventana
        self._ventana.geometry("800x700")  # Establece el tamaño de la ventana

        self.create_widgets()  # Llama a la función para crear los componentes de la interfaz
        self.df = pd.DataFrame()  # Inicializa un DataFrame vacío para almacenar datos
        self.original_df = pd.DataFrame()  # Inicializa un DataFrame para almacenar los datos originales

    def create_widgets(self):
        """Crea los widgets (componentes) de la interfaz gráfica."""
        # Etiqueta principal
        etiqueta1 = tk.Label(self._ventana, text="DATA EXPLORER", bg="turquoise", font=("Arial", 16))
        etiqueta1.pack(pady=10)  # Empaqueta la etiqueta en la ventana

        # Botón para buscar archivos
        boton_buscar = tk.Button(self._ventana, text="Pulse para buscar un archivo", font=("Arial", 12),
                                 command=self.buscar_archivo, padx=20, pady=10)
        boton_buscar.pack(pady=10)  # Empaqueta el botón en la ventana

        # Etiqueta para indicar al usuario sobre la carga de datos
        etiqueta2 = tk.Label(self._ventana, text="Los datos se cargarán en el espacio y la ruta del archivo seleccionado se indicará a seguir")
        etiqueta2.pack(pady=10)

        self.ruta_archivo = tk.StringVar()  # Variable para almacenar la ruta del archivo (StringVar almacena cadenas de texto)
        self.ruta_archivo.set("No hay ningún archivo seleccionado.")  # Establece el texto inicial

        # Etiqueta que muestra la ruta del archivo seleccionado
        etiqueta_ruta = tk.Label(self._ventana, textvariable=self.ruta_archivo, bg="lightgray", wraplength=550)
        etiqueta_ruta.pack(padx=10, pady=5)

        # Marco para la tabla de datos
        self._frame_tabla = tk.Frame(self._ventana, width=500, height=300)  # Frame es un contenedor que agrupa widgets 
        self._frame_tabla.pack(fill=tk.BOTH, padx=10, pady=15)

        self._tabla = ScrollTable(self._frame_tabla)  # Crea una instancia de ScrollTable

        # Botón para detectar valores inexistentes
        self.boton_detectar_nan = tk.Button(self._ventana, text="Detectar valores inexistentes", command=self.detectar_nan)
        self.boton_detectar_nan.pack(pady=10)

        # Botón para abrir la ventana de manejo de datos inexistentes
        self.boton_manejo_nan = tk.Button(self._ventana, text="Pulse para seleccionar el manejo de datos inexistentes", 
                                            command=self.abrir_ventana_manejo_nan)
        self.boton_manejo_nan.pack(pady=10)

        # Botón para restaurar la tabla inicial
        self.boton_reset = tk.Button(self._ventana, text="Volver a tabla inicial con datos inexistentes", command=self.resetear_tabla)
        self.boton_reset.pack(pady=10)

    def abrir_ventana_manejo_nan(self):
        """Abre una nueva ventana para manejar los datos inexistentes."""
        if self.df.empty:  # Verifica si no hay datos cargados
            messagebox.showwarning("Advertencia", "Debes seleccionar un archivo primero.")  # Muestra advertencia
            return  # Sale de la función

        # Crea una nueva ventana para manejar datos inexistentes
        self.ventana_manejo_nan = tk.Toplevel(self._ventana)  #Toplevel se usa para crear ventanas separadas de la principal
        self.ventana_manejo_nan.title("Manejo de Datos Inexistentes")
        self.ventana_manejo_nan.geometry("400x200")

        # Etiqueta que explica al usuario qué hacer
        etiqueta3 = tk.Label(self.ventana_manejo_nan, text="Selecciona el tipo de manejo de datos inexistentes.")
        etiqueta3.pack(pady=10)

        # Menú desplegable para seleccionar el método de preprocesamiento
        self.method_var = tk.StringVar()  
        self.method_dropdown = ttk.Combobox(self.ventana_manejo_nan, textvariable=self.method_var, state="readonly", width=40)  # ComboBox crea el desplegable 
        self.method_dropdown['values'] = ("Eliminar Filas", "Rellenar con Media", "Rellenar con Mediana", "Rellenar con Valor Constante")  # Opciones del menú
        self.method_dropdown.pack(pady=10)

        # Entrada para el valor constante, inicialmente oculta
        self.valor_entrada_cte = tk.Entry(self.ventana_manejo_nan, width=40)
        self.valor_entrada_cte.pack(pady=5)  
        self.valor_entrada_cte.pack_forget()  # Oculta la entrada inicialmente

        # Etiqueta para el valor constante
        self.etiqueta_constante = tk.Label(self.ventana_manejo_nan, text="Ingrese el valor de la constante:")
        
        # Botón para aplicar el preprocesado
        self.apply_button = tk.Button(self.ventana_manejo_nan, text="Aplicar Preprocesado", command=self.aplicar_preprocesado)
        self.apply_button.pack(pady=10)

        # Vincula el evento de selección del menú desplegable con la función que muestra/oculta la entrada
        self.method_dropdown.bind("<<ComboboxSelected>>", self.entrada_cte)  # bind asocia un evento específico con una función 

    def buscar_archivo(self):
        """Permite al usuario buscar un archivo y cargarlo en el programa."""
        filetypes = (
            ("Todos los archivos compatibles (CSV, EXCEL, SQL)", "*.csv *.xlsx *.xls *.db *.sqlite"),  # Tipos de archivos permitidos
        )
        # Abre el diálogo para seleccionar un archivo
        archivo = filedialog.askopenfilename(title="Buscar archivo", filetypes=filetypes) # filedialog.askopenfilename sentnecia que abre el buscador 

        if archivo:  # Si se seleccionó un archivo
            df = open_files.open_file(archivo)  # Llama a la función para abrir el archivo
            if df is not None:  # Si el archivo se carga correctamente
                messagebox.showinfo("Éxito", "El archivo se ha leído correctamente.")  # Muestra mensaje de éxito
                self.ruta_archivo.set(f"Archivo seleccionado: {archivo}")  # Actualiza la ruta del archivo en la interfaz
                self.df = df  # Guarda el DataFrame cargado
                self.original_df = df.copy()  # Crea una copia del DataFrame original
                self.mostrar_datos(df)  # Muestra los datos en la tabla
        else:
            messagebox.showwarning("Advertencia", "No has seleccionado ningún archivo.")  # Muestra advertencia si no se selecciona un archivo

    def mostrar_datos(self, df):
        """Muestra los datos en la tabla."""
        self._tabla.empty_table()  # Limpia la tabla antes de mostrar nuevos datos
        self._tabla.create_from_df(df)  # Crea la tabla a partir del DataFrame
        self._tabla.show()  # Muestra la tabla en la interfaz

    def aplicar_preprocesado(self):
        """Aplica el preprocesado seleccionado en el menú desplegable y actualiza la tabla."""
        if self.df.empty:  # Verificación para asegurarse de que hay un archivo cargado
            messagebox.showwarning("Advertencia", "Debes seleccionar un archivo primero.")  # Muestra advertencia
            return  # Sale de la función

        method = self.method_var.get()  # Obtiene el método seleccionado en el menú
        self.df = self.original_df.copy()  # Restaura el DataFrame original para aplicar el preprocesado

        # Aplica el método de preprocesamiento seleccionado
        if method == "Eliminar Filas":
            self.df.dropna(inplace=True)  # dropna elimina filas con valores inexistentes
        elif method == "Rellenar con Media":
            self.df.fillna(self.df.mean(), inplace=True)  # Rellena con la media. fillna rellena los campos de nan con lo que le indiques 
        elif method == "Rellenar con Mediana":
            self.df.fillna(self.df.median(), inplace=True)  # Rellena con la mediana
        elif method == "Rellenar con Valor Constante":
            constant_value = self.valor_entrada_cte.get()  # Obtiene el valor constante de la entrada

            try:
                constant_value = float(constant_value)  # Intenta convertir el valor a float
                self.df.fillna(constant_value, inplace=True)  # Rellena con el valor constante
            except ValueError:
                messagebox.showwarning("Advertencia", "Debes ingresar un número válido.")  # Muestra advertencia si el valor no es válido
                return  # Sale de la función

        self.mostrar_datos(self.df)  # Muestra la tabla actualizada con los datos preprocesados
        messagebox.showinfo("Éxito", "Preprocesado aplicado correctamente.")  # Muestra mensaje de éxito

        # Cerrar la ventana de manejo de NaN
        self.ventana_manejo_nan.destroy()  # destroy cierra la ventana de manejo de datos inexistentes

    def detectar_nan(self):
        """Detecta y muestra cuántos valores inexistentes hay en el DataFrame."""
        if self.df.empty:  # Verificación para asegurarse de que hay un archivo cargado
            messagebox.showwarning("Advertencia", "Debes seleccionar un archivo primero.")  # Muestra advertencia
            return  # Sale de la función

        missing_info = self.df.isnull().sum()  # Calcula el número de valores inexistentes por columna
        missing_columns = missing_info[missing_info > 0]  # Filtra columnas con valores inexistentes
        
        if not missing_columns.empty:  # Si hay columnas con valores inexistentes
            message = "Valores inexistentes detectados en las siguientes columnas:\n"
            for col, count in missing_columns.items():  # Itera sobre las columnas con valores faltantes
                message += f"- {col}: {count} valores faltantes\n"
            messagebox.showinfo("Valores Inexistentes", message)  # Muestra mensaje con la información
        else:
            messagebox.showinfo("Valores Inexistentes", "No se detectaron valores inexistentes.")  # Mensaje si no hay valores faltantes

    def entrada_cte(self, event):
        """Muestra u oculta la entrada de valor constante según la opción seleccionada."""
        if self.method_var.get() == "Rellenar con Valor Constante":
            self.etiqueta_constante.pack()  # Muestra la etiqueta para el valor constante
            self.valor_entrada_cte.pack()  # Muestra la entrada para el valor constante
        else:
            self.etiqueta_constante.pack_forget()  # Oculta la etiqueta si no se necesita
            self.valor_entrada_cte.pack_forget()  # Oculta la entrada si no se necesita

    def resetear_tabla(self):
        """Restaura la tabla a su estado inicial."""
        if self.original_df.empty:  # Verifica si hay datos originales
            messagebox.showwarning("Advertencia", "No hay datos iniciales para restaurar.")  # Muestra advertencia
            return  # Sale de la función

        self.df = self.original_df.copy()  # Actualiza el DataFrame actual con los datos originales
        self.mostrar_datos(self.original_df)  # Muestra los datos originales en la tabla


# Inicializa y ejecuta la aplicación
if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal
    app = DataExplorerApp(root)  # Crea una instancia de la aplicación
    root.mainloop()  # Ejecuta el bucle principal de la interfaz gráfica
