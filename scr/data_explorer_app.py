import tkinter as tk  
from tkinter import messagebox, filedialog, ttk  
import open_files 
from scroll_table import ScrollTable

# Clase principal para gestionar la interfaz gráfica
class DataExplorerApp:
    # HABRÁ QUE HACER EN EL FUTURO GETTERS PARA LOS ATRIBUTOS QUE LO NECESITEN
    def __init__(self, ventana):
        self._ventana = ventana
        self._ventana.title("Data Explorer")
        self._ventana.geometry("600x600")
 
        # Llamamos al método para crear los widgets de la ventana
        self.create_widgets()
 
    def create_widgets(self):
        # Etiqueta principal
        etiqueta = tk.Label(self._ventana, text="DATA EXPLORER", bg="turquoise", font=("Arial", 16))
        etiqueta.pack(pady=10)
 
        # Botón para abrir el explorador de archivos
        boton_buscar = tk.Button(self._ventana, text="Presiona para buscar un archivo", font=("Arial", 12),
                                 command=self.buscar_archivo, padx=20, pady=10)
        boton_buscar.pack(pady=10)
 
        # Etiqueta informativa
        etiqueta2 = tk.Label(self._ventana, text="Los datos se cargarán en el espacio y la ruta del archivo seleccionado se indicará a seguir")
        etiqueta2.pack(pady=10)
 
        # Variable para almacenar la ruta del archivo seleccionado
        self.ruta_archivo = tk.StringVar()
        self.ruta_archivo.set("No hay ningún archivo seleccionado.")
        etiqueta_ruta = tk.Label(self._ventana, textvariable=self.ruta_archivo, bg="lightgray", wraplength=550)
        etiqueta_ruta.pack(padx=10, pady=5)

        # Creamos un frame para la tabla de datos y las barras de desplazamiento
        self._frame_tabla = tk.Frame(self._ventana, width=500, height=300)  # Establecer dimensiones
        self._frame_tabla.pack(fill=tk.BOTH, padx=10, pady=15)

        self._tabla = ScrollTable(self._frame_tabla)  # Tabla donde aparecen los datos

    def buscar_archivo(self):
        filetypes = (
            ("Todos los archivos compatibles (CSV, EXCEL, SQL)", 
            "*.csv *.xlsx *.xls *.db *.sqlite"),
        )
        archivo = filedialog.askopenfilename(
            title="Buscar archivo",
            filetypes=filetypes) 

        if archivo:
            df = open_files.open_files_interface(archivo)
            if df is not None:
                messagebox.showinfo("Éxito", "El archivo se ha leído correctamente.")
                self.ruta_archivo.set(f"Archivo seleccionado: {archivo}")
                self.mostrar_datos(df)
        else:
            messagebox.showwarning("Advertencia", "No has seleccionado ningún archivo.")

    def mostrar_datos(self, df):
        self._tabla.empty_table()
        self._tabla.create_from_df(df)
        self._tabla.show()
