import tkinter as tk  
from tkinter import messagebox, filedialog, ttk  
from open_files import open_files_interface
from scroll_table import ScrollTable
from column_menu import MenuManager

class ScrollApp:
    def __init__(self, window):

        self._file = None  # Variable para hacer operaciones con el path
        self._file_path = tk.StringVar()  # Variable para mostrar el path por pantalla

        self._window = window

        # Dimensiones de la ventana en función del tamaño de la pantalla
        self._width = self._window.winfo_screenwidth() //2
        self._height = self._window.winfo_screenheight()  //2
        # Para que salga centrada en la pantalla
        self._x = self._width//2
        self._y = self._height//3

        self._window.title("Linear Regression App")
        self._window.geometry(f"{self._width}x{self._height}+{self._x}+{self._y}")

        # Crear un main frame
        self._main_frame = tk.Frame(self._window)
        self._main_frame.pack(fill="both", expand=True)

        # header está fuera del área de scroll
        self.header()

        # Crear un canvas
        self._my_canvas = tk.Canvas(self._main_frame)
        self._my_canvas.pack(side="left", fill="both", expand=True)

        # Añadir un scrollbar al canvas
        my_scroll_bar = ttk.Scrollbar(self._main_frame, orient="vertical", command=self._my_canvas.yview)
        my_scroll_bar.pack(side="right", fill="y")

        # Configurar el canvas
        self._my_canvas.configure(yscrollcommand=my_scroll_bar.set)
        self._my_canvas.bind("<Configure>", lambda e: self._my_canvas.configure(scrollregion = self._my_canvas.bbox("all")))

        # Crear otro frame dentro del canvas
        # En este es donde se añaden el resto de widgets
        self._second_frame = tk.Frame(self._my_canvas)
        
        # Añadir el nuevo frame a la window dentro del canvas
        self._my_canvas.create_window((0, 0), window=self._second_frame, anchor="nw")
        # Si en window = especificamos width y height, el área de scroll tendrá esas dimensiones
        # Si no, se adapta a los widgets que tenga dentro
        # Importante: no tocar width, porque esta va depende del tamaño de la tabla
        # y ese frame se ajusta solo al redimensionar la ventana
        #, width = self._width-13)

        # Aplicación principal con self._second_frame como frame principal
        # Pasamos self._my_canvas para ajustar el área de scroll a medida que se añaden widgets
        # Pasamos self para acceder desde dentro de la clase a las dimensiones de la ventana y ajustar la tabla de datos
        self._app = App(self._second_frame, self._my_canvas, self)

    # Necesitamos acceder a la ventana desde otro objeto para acceder a sus dimensiones
    @property
    def window(self):
        return self._window
    
    def search_file(self,event = None):
        filetypes = (
            ("Todos los archivos compatibles (CSV, EXCEL, SQL)", 
            "*.csv *.xlsx *.xls *.db *.sqlite"),
            )
        self._file = filedialog.askopenfilename(
            title="Buscar archivo",
            filetypes=filetypes) 

        if self._file:
            text = self.shorten_route_text(self._file)
            self._file_path.set(f"Archivo seleccionado: {text}")        
        else:
            messagebox.showwarning("Advertencia", "No has seleccionado ningún archivo.")

    def open_file(self):
        if self._file:  # Verificar si hay un archivo seleccionado
            self._data = open_files_interface(self._file)
            if self._data is not None:
                messagebox.showinfo("Éxito", "El archivo se ha leído correctamente.")
                # Actualiza los datos
                self._app.data = self._data
                # Muestra los datos
                self._app.show_data()  # Llamar a show_data con el DataFrame cargado
            else:
                messagebox.showwarning("Error", "No se pudo cargar el archivo.")
        else:  # Si no hay ningún archivo seleccionado
            messagebox.showwarning("Advertencia", "No hay ningún archivo seleccionado.")
    
    def shorten_route_text(self, text):
        """Recorta el texto de la ruta si excede el número máximo de caracteres."""
        max_chars = 50

        if len(text) > max_chars:
            truncated_text = "..." + text[-max_chars:]
        else:
            truncated_text = text

        return truncated_text
    
    def header(self):

        # Se crea una frame para situar la etiqueta path, la ruta del archivo y el botón de abrir
        header_frame = tk.Frame(self._main_frame, bg = '#d0d7f2', height = 40, width = 682)
        header_frame.pack(fill = tk.X, side='top')
        header_frame.pack_propagate(False)
    
        # Label de path
        label = tk.Label(header_frame, text = "Path", fg="#6677B8",bg = '#d0d7f2', font=("Arial", 14,'bold'))
        label.pack(side='left', padx=(10,20), pady=5 ) 

        # Variable para almacenar la ruta del file seleccionado y botón para seleccionarlo
        self._file_path.set("Haz click para seleccionar un archivo")
        path_label = tk.Label(header_frame, textvariable= self._file_path, fg= "#FAF8F9", bg = '#6677B8',
                                font= ("DejaVu Sans Mono", 11), activebackground= "#808ec6",
                                activeforeground= "#FAF8F9", cursor= "hand2",width = 55)
        path_label.bind("<Button-1>", self.search_file)
        path_label.pack(side='left', pady=5)

        # Botón para abrir el explorador de archivos 
        search_button = tk.Button(header_frame, text="Abrir", font=("Arial", 12,'bold'),
                                  fg="#FAF8F9", bg = '#6677B8' ,activebackground="#808ec6",activeforeground="#FAF8F9",
                                  cursor="hand2", command= self.open_file , padx=20, pady=10)
        search_button.pack(side='right', padx=10, pady=5) 
        
        # Una línea de separador por estética
        separator = tk.Frame(self._main_frame, bg = '#6677B8', height=3)
        separator.pack(fill = tk.X, side='top', pady=(0, 10) )

        self._main_frame.pack(fill=tk.BOTH, expand=True)

    def update(self):
        # Actualizar la interfaz gráfica antes de ajustar la región de scroll
        self._second_frame.update_idletasks()
        # Actualizar el scroll region después de añadir nuevos botones
        self._my_canvas.configure(scrollregion=self._my_canvas.bbox("all"))

########################################################################################

# Clase principal para gestionar la interfaz gráfica
class App:
    # HABRÁ QUE HACER EN EL FUTURO GETTERS PARA LOS ATRIBUTOS QUE LO NECESITEN
    def __init__(self, frame, canvas, scroll_window):

        # Frame donde irá la tabla
        # En realidad se redefine luego, pero hay que inicializarlo antes de añadir el 
        # evento a la ventana porque si no sale un error diciendo que no existe
        self._table_frame = tk.Frame()  

        self._frame = frame
        self._canvas = canvas

        self._scroll_window = scroll_window
        # Evento cuando se cambia el tamaño de la ventana
        self._scroll_window.window.bind("<Configure>", self.on_window_resize)
        
        self._table = None # Futuro objeto Tabla

        self._file = None  # Variable para hacer operaciones con el path
        self._file_path = tk.StringVar()  # Variable para mostrar el path por pantalla

        # DataFrame que nunca se modificará
        # Solo se sobreescribe cuando se elige un archivo nuevo
        self._data = None  
        # DataFrame con los datos preprocesados
        # Se sobreescribe cuando se elige un método distinto de preprocesado
        self._processed_data = None 

    @property
    def data(self):
        return self._data
    
    # Para poder actualizar el DataFrame al leer el archivo desde la clase ScrollApp
    @data.setter
    def data(self, df):
        self._data = df

    def show_data(self):  
        
        # Vacía el frame en el caso de que ya hubiese una tabla anteriormente
        # (lo que ocurre cuando el usuario cambia de archivo)
        self.clear_frame()
    
        # Creamos un frame para la table de data y las barras de desplazamiento
        self._table_frame = tk.Frame(self._frame, height = 400, width = self._scroll_window.window.winfo_width() - 15)  # Establecer dimensiones
        self._table_frame.pack(side= tk.TOP, fill= tk.X, anchor = "center")
        self._table_frame.pack_propagate(False)  # Para que use height como altura de la tabla
        
        self._table = ScrollTable(self._table_frame)  # Tabla con scrollbars donde aparecen los datos

        self._table.empty_table()  # Limpia la tabla por si ya tenía datos
        self._table.create_from_df(self._data)  # Copia los datos del DataFrame a la tabla
        self._table.show()  # Muestra la tabla

        separator = tk.Frame(self._frame, bg = '#6677B8', height = 3)
        separator.pack(fill = tk.X, side = tk.TOP, anchor = "center")

        # Columnas numéricas de la table
        numeric = self._table.numeric_columns()

        # Crear un frame para el selector de columnas
        column_selector_frame = tk.Frame(self._frame, height = 400, width = self._scroll_window.window.winfo_width() - 15)
        column_selector_frame.pack(fill = tk.BOTH, side = tk.TOP, anchor = "center")
        column_selector_frame.pack_propagate(False)
        # Si fijamos el tamaño del frame y hacemos que no pueda reducirse (con propagate = False)
        # No hace falta cambiar de place a pack en el módulo de column_menu

        # Instanciar el MenuManager
        self._menu = MenuManager(column_selector_frame, numeric, self._data)
        self._processed_data = self._menu.new_df  # Actualiza el df procesado
        
        # Para que se actualice el área de scroll
        # Hay que llamar a esta función siempre que creemos un widget nuevo
        # (Habrá que llamarla otra vez después de generar la gráfica)
        self._scroll_window.update()
        
    def clear_frame(self):
        for widget in self._frame.winfo_children():
            widget.destroy()

    def on_window_resize(self, event):
        self._table_frame.config(width= self._scroll_window.window.winfo_width() - 15)

########################################################################################

# Para probar

def main():
    ventana = tk.Tk()  # Ventana principal
    app = ScrollApp(ventana)
    ventana.mainloop()  # Inicia el bucle principal de la aplicación

if __name__ == "__main__":
    main()