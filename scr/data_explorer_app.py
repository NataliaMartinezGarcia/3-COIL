import tkinter as tk  
from tkinter import messagebox, filedialog, ttk  
import open_files 
from scroll_table import ScrollTable
from column_selector import ColumnSelector

# Clase principal para gestionar la interfaz gráfica
class DataExplorerApp:
    # HABRÁ QUE HACER EN EL FUTURO GETTERS PARA LOS ATRIBUTOS QUE LO NECESITEN
    def __init__(self, window):
        self._window = window
        self._window.title("Data Explorer")
        self._window.geometry("700x600")

        self._table = None
 
        # Crear frames para la interfaz
        self._frame_start = tk.Frame(self._window,bg = '#FAF8F9')
        self._frame_data = tk.Frame(self._window,bg = '#FAF8F9')

        # Llamamos al método para crear los widgets de la window
        self.create_widgets_start()
 
    def create_widgets_start(self):
        # label principal
        label = tk.Label(self._frame_start, text = "DATA EXPLORER", fg = "#201528", bg = '#FAF8F9' , font = ("Arial Black", 30,"bold"))
        label.place(relx=0.5, rely=0.45, relwidth = 0.8, anchor='center')  # Centrar label en el medio

 
        # Botón para abrir el explorador de archivos
        search_button = tk.Button(self._frame_start, text="Presiona para buscar un archivo", font=("Arial", 12,'bold'),
                                  fg="#FAF8F9", bg = '#6677B8' ,activebackground="#808ec6",activeforeground="#FAF8F9",
                                  cursor="hand2", command=self.search_file, padx=20, pady=10)
        search_button.place(relx = 0.5,rely=0.55,relwidth = 0.5, anchor= 'center' )  # Centrar botón en el medio

        self._frame_start.pack(fill=tk.BOTH, expand=True)

    def search_file(self):
        filetypes = (
            ("Todos los archivos compatibles (CSV, EXCEL, SQL)", 
            "*.csv *.xlsx *.xls *.db *.sqlite"),
        )
        file = filedialog.askopenfilename(
            title="Buscar archivo",
            filetypes=filetypes) 

        if file:
            df = open_files.open_files_interface(file)
            if df is not None:
                messagebox.showinfo("Éxito", "El archivo se ha leído correctamente.")
                self.show_data(df, file)
        else:
            messagebox.showwarning("Advertencia", "No has seleccionado ningún archivo.")

    def show_data(self, df , file):  
         # Ocultar el frame de start
        self._frame_start.pack_forget()
        
        # Crear y mostrar el frame de data
        self._frame_data.pack(fill=tk.BOTH, expand=True)
        
        # Variable para almacenar la ruta del file seleccionado
        self.file_route = tk.StringVar()
        self.file_route.set(f"Archivo seleccionado: {file}")
        label_route = tk.Label(self._frame_data, textvariable=self.file_route, bg="#d0d7f2", fg="#201528", wraplength=550)
        label_route.place(relx = 0.5, rely = 0.03, anchor = 'center')
    
        # Creamos un frame para la table de data y las barras de desplazamiento
        self._frame_table = tk.Frame(self._frame_data)  # Establecer dimensiones
        self._frame_table.place(rely = 0.29,relx = 0.5,relwidth= 1,relheight= 0.4 ,anchor = "center")

        self._table = ScrollTable(self._frame_table)  # table donde aparecen los data

        self._table.empty_table()
        self._table.create_from_df(df)
        self._table.show()

        self.columns()
       
        # Agregar un botón para regresar al frame de start
        return_button = tk.Button(self._frame_data, text="  Regresar  ", font=("Arial", 10,'bold'),
                                  fg="#FAF8F9", bg = '#6677B8' ,activebackground="#808ec6",activeforeground="#FAF8F9",
                                  cursor="hand2", command=self.restart)
        return_button.pack(pady=5)
        return_button.place(relx=0.5, rely=0.95, anchor='center') 


    def restart(self):      
        self._window.destroy()

        # Reiniciar la aplicación creando una nueva instancia
        root = tk.Tk()
        app = DataExplorerApp(root)
        root.mainloop()

    def columns(self):
        # Columnas numéricas de la table
        numeric = self._table.numeric_columns()

        # Crear un frame para el selector de columnas
        column_selector_frame = tk.Frame(self._frame_data)

        # Instanciar el ColumnSelector
        self._column_selector = ColumnSelector(column_selector_frame, numeric)
        column_selector_frame.place(rely = 0.7,relx = 0.5,relwidth= 1,relheight= 0.4,anchor = "center")