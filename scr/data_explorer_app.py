import tkinter as tk  
from tkinter import messagebox, filedialog, ttk  
import open_files
from scroll_table import ScrollTable
from column_selector import ColumnSelector
 
# Clase principal para gestionar la interfaz gráfica
class DataExplorerApp:
    WIDTH = 900
    HEIGHT = 900
    # HABRÁ QUE HACER EN EL FUTURO GETTERS PARA LOS ATRIBUTOS QUE LO NECESITEN
    def __init__(self, ventana):
        self._ventana = ventana
        self._ventana.title("Data Explorer")
        self._ventana.geometry("900x900")
 
        self._tabla = None
 
        # Crear frames para la interfaz
        self._frame_inicio = tk.Frame(self._ventana,bg = '#FAF8F9')
        self._frame_datos = tk.Frame(self._ventana,bg = '#FAF8F9')
 
        # Llamamos al método para crear los widgets de la ventana
        self.create_widgets_inicio()
 
    def create_widgets_inicio(self):
        # Etiqueta principal
        etiqueta = tk.Label(self._frame_inicio, text = "DATA EXPLORER", fg = "#201528", bg = '#FAF8F9' , font = ("Arial Black", 30,"bold"))
        #etiqueta.pack(pady = (50,20))
        etiqueta.place(relx=0.5, rely=0.45, anchor='center')  # Centrar etiqueta en el medio
 
 
        # Botón para abrir el explorador de archivos
        boton_buscar = tk.Button(self._frame_inicio, text="Presiona para buscar un archivo", font=("Arial", 12,'bold'),
                                  fg="#FAF8F9", bg = '#6677B8' ,activebackground="#808ec6",activeforeground="#FAF8F9",
                                  cursor="hand2", command=self.buscar_archivo, padx=20, pady=10)
        #boton_buscar.pack(pady= (0,50))
        boton_buscar.place(relx=0.5, rely=0.55, anchor='center')  # Centrar botón en el medio
 
        # Etiqueta informativa
        # etiqueta2 = tk.Label(self._frame_inicio, text="Los datos se cargarán en el espacio y la ruta del archivo seleccionado se indicará a seguir")
        # etiqueta2.pack(pady=10)
 
        self._frame_inicio.pack(fill=tk.BOTH, expand=True)
 
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
                self.mostrar_datos(df, archivo)
        else:
            messagebox.showwarning("Advertencia", "No has seleccionado ningún archivo.")
 
    def mostrar_datos(self, df , archivo):  
         # Ocultar el frame de inicio
        self._frame_inicio.pack_forget()
        
        # Crear y mostrar el frame de datos
        self._frame_datos.pack(fill='both', expand=True)
 
        # Variable para almacenar la ruta del archivo seleccionado
        self.ruta_archivo = tk.StringVar()
        self.ruta_archivo.set(f"Archivo seleccionado: {archivo}")
        etiqueta_ruta = tk.Label(self._frame_datos, textvariable=self.ruta_archivo, bg="#d0d7f2", fg="#201528", wraplength=550)
        etiqueta_ruta.pack(padx=10, pady=5)
    
        # Creamos un frame para la tabla de datos y las barras de desplazamiento
        self._frame_tabla = tk.Frame(self._frame_datos, width=500, height=300)  # Establecer dimensiones
        self._frame_tabla.pack(fill=tk.BOTH, padx=10, pady=15)
 
        self._tabla = ScrollTable(self._frame_tabla)  # Tabla donde aparecen los datos
 
        self._tabla.empty_table()
        self._tabla.create_from_df(df)
        self._tabla.show()
 
        # Agregar un botón para regresar al frame de inicio
        boton_regresar = tk.Button(self._frame_datos, text="  Regresar  ", font=("Arial", 10,'bold'),
                                  fg="#FAF8F9", bg = '#6677B8' ,activebackground="#808ec6",activeforeground="#FAF8F9",
                                  cursor="hand2", command=self.reinicio)
        boton_regresar.pack(pady=10)
 
        # Llamar a la función para crear el selector de columnas debajo del botón de regresar
        self.desplegables()
 
    def reinicio(self):
         
        self._ventana.destroy()
 
        # Reiniciar la aplicación creando una nueva instancia
        root = tk.Tk()
        app = DataExplorerApp(root)
        root.mainloop()
 
    def desplegables(self):
        # Columnas numéricas de la tabla
        numeric = self._tabla.numeric_columns()
 
        # Crear un frame para el selector de columnas
        column_selector_frame = tk.Frame(self._frame_datos, width=400, height=400)
        column_selector_frame.pack(padx=10, pady=10, fill=tk.X)
 
        # Instanciar el ColumnSelector
        # Añadir el dataframe de la tabla
        self._column_selector = ColumnSelector(column_selector_frame, numeric, self._tabla.data)
        column_selector_frame.pack(fill='x')