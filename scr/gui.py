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
        self._window.title("Linear Regression App")
        self._window.geometry("700x600")

        self._table = None
        self.file = None
        self.file_route = tk.StringVar()

        self._frame = tk.Frame(self._window,bg = '#FAF8F9')
        self.scrollbar = tk.Scrollbar(self._window, orient="vertical")
        self.scrollbar.place(relx = 1,relheight= 1, anchor= 'ne')

        # Llamamos al método para crear los widgets de la window
        self.header()

    def search_file(self,event = None):
        filetypes = (
            ("Todos los archivos compatibles (CSV, EXCEL, SQL)", 
            "*.csv *.xlsx *.xls *.db *.sqlite"),
        )
        file = filedialog.askopenfilename(
            title="Buscar archivo",
            filetypes=filetypes) 

        if file:
            self.file = file
            self.file_route.set(f"Archivo seleccionado: {file}")               
        else:
            messagebox.showwarning("Advertencia", "No has seleccionado ningún archivo.")

    def open_file(self):
        if self.file:  # Verificar si hay un archivo seleccionado
            df = open_files.open_files_interface(self.file)
            if df is not None:
                messagebox.showinfo("Éxito", "El archivo se ha leído correctamente.")
                self.show_data(df)  # Llamar a show_data con el DataFrame cargado
            else:
                messagebox.showwarning("Error", "No se pudo cargar el archivo.")
        else:
            messagebox.showwarning("Advertencia", "No hay ningún archivo seleccionado.")

    def header(self):
        # Se crea una frame para situar la etiqueta path, la ruta del archivo y el botón de abrir
        header_frame = tk.Frame(self._frame, bg = '#d0d7f2')
        header_frame.place (relwidth= 1, relheight= 0.05)
    
        # Label de path
        label = tk.Label(header_frame, text = "Path", fg="#6677B8",bg = '#d0d7f2', font=("Arial", 14,'bold'))
        label.place(relx=0.1,rely = 0.5, relheight=1 , anchor='center') 

        # Variable para almacenar la ruta del file seleccionado y botón para seleccionarlo
        self.file_route.set("Haz click para seleccionar un archivo")
        route_label = tk.Label(header_frame, textvariable= self.file_route, fg= "#FAF8F9", bg = '#6677B8',
                                font= ("DejaVu Sans Mono", 11), activebackground= "#808ec6",
                                activeforeground= "#FAF8F9", cursor= "hand2")
        route_label.bind("<Button-1>", self.search_file)
        route_label.place(relx = 0.5, rely = 0.45, anchor = 'center')
    
        # Botón para abrir el explorador de archivos 
        search_button = tk.Button(header_frame, text="Abrir", font=("Arial", 12,'bold'),
                                  fg="#FAF8F9", bg = '#6677B8' ,activebackground="#808ec6",activeforeground="#FAF8F9",
                                  cursor="hand2", command= self.open_file , padx=20, pady=10)
        search_button.place(relx = 0.9, rely=0.45, relwidth = 0.1,relheight= 0.8, anchor= 'center' ) 
        
        # Una línea de separador por estética
        separator = tk.Frame(self._frame, bg = '#6677B8')
        separator.place(rely = 0.05, relwidth = 1, relheight = 0.004, anchor= 'w')
        
        self._frame.pack(fill=tk.BOTH, expand=True)

    def show_data(self, df):  
        # Creamos un frame para la table de data y las barras de desplazamiento
        table_frame = tk.Frame(self._frame)  # Establecer dimensiones
        table_frame.place(rely = 0.254,relx = 0.5,relwidth= 1,relheight= 0.4 ,anchor = "center")

        self._table = ScrollTable(table_frame)  # table donde aparecen los data

        self._table.empty_table()
        self._table.create_from_df(df)
        self._table.show()

        separator = tk.Frame(self._frame, bg = '#6677B8')
        separator.place(rely = 0.454, relwidth = 1, relheight = 0.004, anchor= 'w')
 
        # Columnas numéricas de la table
        numeric = self._table.numeric_columns()

        # Crear un frame para el selector de columnas
        column_selector_frame = tk.Frame(self._frame)
        column_selector_frame.place(rely = 0.456,relx = 0.5,relwidth= 1,relheight= 0.5,anchor = "n")

        # Instanciar el ColumnSelector
        self._column_selector = ColumnSelector(column_selector_frame, numeric)

########################################################
# Para probar la estética (ignorad esto)

def main():
    ventana = tk.Tk()  # Ventana principal
    app = DataExplorerApp(ventana)
    ventana.mainloop()  # Inicia el bucle principal de la aplicación

if __name__ == "__main__":
    main()