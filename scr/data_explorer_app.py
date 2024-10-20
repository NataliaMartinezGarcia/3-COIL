import tkinter as tk  
from tkinter import messagebox, filedialog, ttk  
import open_files 
from scroll_table import ScrollTable
from column_selector import ColumnSelector

# Clase principal para gestionar la interfaz gráfica
class DataExplorerApp:
    # HABRÁ QUE HACER EN EL FUTURO GETTERS PARA LOS ATRIBUTOS QUE LO NECESITEN
    def __init__(self, ventana):
        self._ventana = ventana
        self._ventana.title("Data Explorer")
        self._ventana.geometry("700x600")

        self._tabla = None
 
        # Crear frames para la interfaz
        self._frame_inicio = tk.Frame(self._ventana,bg = '#FAF8F9')
        self._frame_datos = tk.Frame(self._ventana,bg = '#FAF8F9')

        # Llamamos al método para crear los widgets de la ventana
        self.create_widgets_inicio()
 
    def create_widgets_inicio(self):
        # Etiqueta principal
        etiqueta = tk.Label(self._frame_inicio, text = "DATA EXPLORER", fg = "#201528", bg = '#FAF8F9' , font = ("Arial Black", 30,"bold"))
        etiqueta.place(relx=0.5, rely=0.45, relwidth = 0.8, anchor='center')  # Centrar etiqueta en el medio

 
        # Botón para abrir el explorador de archivos
        boton_buscar = tk.Button(self._frame_inicio, text="Presiona para buscar un archivo", font=("Arial", 12,'bold'),
                                  fg="#FAF8F9", bg = '#6677B8' ,activebackground="#808ec6",activeforeground="#FAF8F9",
                                  cursor="hand2", command=self.buscar_archivo, padx=20, pady=10)
        boton_buscar.place(relx = 0.5,rely=0.55,relwidth = 0.5, anchor= 'center' )  # Centrar botón en el medio

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
        self._frame_datos.pack(fill=tk.BOTH, expand=True)
        
        # Variable para almacenar la ruta del archivo seleccionado
        self.ruta_archivo = tk.StringVar()
        self.ruta_archivo.set(f"Archivo seleccionado: {archivo}")
        etiqueta_ruta = tk.Label(self._frame_datos, textvariable=self.ruta_archivo, bg="#d0d7f2", fg="#201528", wraplength=550)
        etiqueta_ruta.place(relx = 0.5, rely = 0.03, anchor = 'center')
    
        # Creamos un frame para la tabla de datos y las barras de desplazamiento
        self._frame_tabla = tk.Frame(self._frame_datos)  # Establecer dimensiones
        self._frame_tabla.place(rely = 0.29,relx = 0.5,relwidth= 1,relheight= 0.4 ,anchor = "center")

        self._tabla = ScrollTable(self._frame_tabla)  # Tabla donde aparecen los datos

        self._tabla.empty_table()
        self._tabla.create_from_df(df)
        self._tabla.show()

        self.desplegables()
       
        # Agregar un botón para regresar al frame de inicio
        boton_regresar = tk.Button(self._frame_datos, text="  Regresar  ", font=("Arial", 10,'bold'),
                                  fg="#FAF8F9", bg = '#6677B8' ,activebackground="#808ec6",activeforeground="#FAF8F9",
                                  cursor="hand2", command=self.reinicio)
        boton_regresar.pack(pady=5)
        boton_regresar.place(relx=0.5, rely=0.95, anchor='center') 


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
        column_selector_frame = tk.Frame(self._frame_datos)
        #column_selector_frame.place(rely = 0.7,relx = 0.5,relwidth= 1,relheight= 0.5,anchor = "center")

        # Instanciar el ColumnSelector
        self._column_selector = ColumnSelector(column_selector_frame, numeric)
        column_selector_frame.place(rely = 0.7,relx = 0.5,relwidth= 1,relheight= 0.4,anchor = "center")

        #column_selector_frame.pack(fill='x') 

        # Falta por resolver que los desplegables se muestren antes de pinchar en la zona donde deberian estar
        # y que el boton de confirmar no se mueva a la derecha al elegir seleccion multiple