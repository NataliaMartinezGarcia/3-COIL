import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
 
# Clase que implementa la interfaz para seleccionar columnas de entrada y salida
class ColumnSelector:
    # Tipos de regresión
    # Constantes. Se hace aquí para que si hay que cambiarlas no tenga que hacerse en todo el código
    SIMPLE = "Simple"
    MULTIPLE = "Múltiple"
    SIMPLE_LABEL = "Selecciona la columna de entrada (feature):"
    MULTIPLE_LABEL = "Selecciona las columnas de entrada (features):"
 
    def __init__(self, frame, columns, df):
        self._frame = frame  # Frame donde estarán los desplegables
        self._columns = columns  # Columnas a elegir
        self._df = df  # DataFrame del que se eligen las columnas
       
        # Tipos de regresión a elegir por el usuario
        # Usa los strings constantes definidos arriba
        self._regression_types = [ColumnSelector.SIMPLE, ColumnSelector.MULTIPLE]
        
        # Tipo de regresión elegido
        # Por defecto el tipo de regresión es simple
        self._selected_regression_type = self._regression_types[0]
 
        # Variable que se mostrará en la etiqueta encima del selector de features
        # Cambiará en función de si es simple o multiple
        self._regression_type_text = tk.StringVar()  # Etiqueta que se actualiza
        self._regression_type_text.set(ColumnSelector.SIMPLE_LABEL)
 
        # Variables para almacenar las selecciones
        self._selected_features = []
        self._selected_target = None
 
        # Estas funciones son simplemente para que no se ponga todo el código en el init
        # Como el create_widgets de las otras clases
        self.create_regression_selector()  # Función que crea el selector de tipo de regresión
        self.create_features_selector()  # Función que crea el selector de features
        self.create_target_selector()  # Función que crea el selector de target
        self.create_confirm_button()  # Función que crea el botón de confirmar
    
    # Getter para obtener las features desde fuera de la clase
    @property    
    def selected_features(self):
        return self._selected_features
 
    # Getter para obtener el target desde fuera de la clase
    @property    
    def selected_target(self):
        return self._selected_target
   
    def create_regression_selector(self):
        """Crea un desplegable para elegir el tipo de regresión lineal."""
 
        label = tk.Label(self._frame, text="Tipo de regresión:")
        label.pack(side='top', padx=5, pady=5)
 
        # Combobox para seleccionar entre regresión simple o múltiple
        # Le pasamos la lista de constantes definida arriba
        self._regression_type_combobox = ttk.Combobox(self._frame, values=self._regression_types, state="readonly")
        self._regression_type_combobox.pack(side='top', padx=5, pady=5)
        self._regression_type_combobox.set(self._regression_types[0])  # Valor predeterminado
 
        # Cada vez que ocurra un evento (en este caso elegir algo nuevo en el combobox)
        # Se actualiza el listbox que da a elegir las features (dejará elegir solo una o varias)
        self._regression_type_combobox.bind("<<ComboboxSelected>>", self.update_regression_type)
 
    def update_regression_type(self, event=None):
        """Actualizar el modo de selección en el Listbox según el tipo de regresión seleccionado."""
 
        # Obtener el tipo de regresión seleccionado y lo guarda en una variable
        # Por defecto era simple
        self._selected_regression_type = self._regression_type_combobox.get()  
 
        # Según el valor de esa variable hace que deje elegir una columna o varias
        if self._selected_regression_type == self._regression_types[0]:  # Si es simple
            self._feature_listbox.config(selectmode=tk.SINGLE)
            self._regression_type_text.set(ColumnSelector.SIMPLE_LABEL)
        else:  # Si es múltiple
            self._feature_listbox.config(selectmode=tk.MULTIPLE)
            self._regression_type_text.set(ColumnSelector.MULTIPLE_LABEL)
 
        # Limpiar que hubiese antes en el listbox
        self._feature_listbox.selection_clear(0, tk.END)
        self._selected_features = []  # Reiniciar la lista de selecciones
 
    def create_features_selector(self):
        """Crea una ListBox para elegir una o varias columnas de entrada o features."""
        features_frame = tk.Frame(self._frame, width=280, height=170)
        features_frame.pack(side='left', padx=10, pady=5)
 
        # Etiqueta que indica si se deben elegir 1 o más columnas
        label = tk.Label(features_frame, textvariable=self._regression_type_text)
        label.place(relx=0.5, rely=0.1, relwidth=1, anchor="center")
       
        # Listbox donde se elegirán esas columnas
        self._feature_listbox = tk.Listbox(features_frame, selectmode=tk.SINGLE, height=5, exportselection=False)
        # exportselection=False -> para que las selecciones no se borren al interactuar con
        # otro widget que no sea el botón de confirmar
        self._feature_listbox.place(relx=0.1, rely=0.4, relwidth=0.75, anchor="w")
 
        # Barra de desplazamiento vertical para cuando haya muchas columnas
        scrollbar = tk.Scrollbar(features_frame, orient="vertical")
        scrollbar.config(command=self._feature_listbox.yview)
        scrollbar.place(relx=0.8, rely=0.4, relheight=0.5, anchor="w")
        self._feature_listbox.config(yscrollcommand=scrollbar.set)
 
        # Ahora mismo la listbox está vacía
        # Le metemos las columnas que nos han pasado
        for column in self._columns:
            self._feature_listbox.insert(tk.END, column)
 
    def create_target_selector(self):
        """Crea un ListBox para elegir la columna de salida o target."""
        
        target_frame = tk.Frame(self._frame, width=280, height=170)
        target_frame.pack(side='right', padx=10, pady=5)
 
        # Etiqueta que indica que se debe elegir 1 columna
        label = tk.Label(target_frame, text="Selecciona la columna de salida (target):")
        label.place(relx=0.5, rely=0.1, relwidth=1, anchor="center")
 
        # Listbox donde se dan a elegir las columnas
        self._target_listbox = tk.Listbox(target_frame, selectmode=tk.SINGLE, height=5)
        self._target_listbox.place(relx=0.1, rely=0.4, relwidth=0.75, anchor="w")
 
        # Barra de desplazamiento vertical para cuando haya muchas columnas
        scrollbar = tk.Scrollbar(target_frame, orient="vertical")
        scrollbar.config(command=self._target_listbox.yview)
        scrollbar.place(relx=0.8, rely=0.4, relheight=0.5, anchor="w")
        self._target_listbox.config(yscrollcommand=scrollbar.set)
 
        # Ahora mismo la listbox está vacía
        # Le metemos las columnas que nos han pasado
        for column in self._columns:
            self._target_listbox.insert(tk.END, column)
 
    def create_confirm_button(self):
        confirm_button = tk.Button(self._frame, text="Confirmar selección", command=self.confirm_selection)
        confirm_button.place(relx=0.5, rely=0.85, anchor='center')

        # Botón para detectar número de NaN
        nan_button = tk.Button(self._frame, text="Detectar número de NaN", command=self.show_nan_count)
        nan_button.place(relx=0.5, rely=0.95, anchor='center')

    def confirm_selection(self):
        """Botón para confirmar las selecciones."""
 
        # Obtiene las features seleccionadas en el listbox
        # Es una lista que tendrá 1 solo elemento si solo se ha elegido 1 (simple)
        # y varios elementos si se ha elegido más de 1 (múltiple)
        self._selected_features = [self._feature_listbox.get(i) for i in self._feature_listbox.curselection()]
 
        # Obtiene el target seleccionado
        # Solo hay una posible elección
        self._selected_target = [self._target_listbox.get(i) for i in self._target_listbox.curselection()]
 
        """
        selected_target_index = self._target_listbox.curselection()
        if selected_target_index:
            self._selected_target = self._columns[selected_target_index[0]]
        else:
            self._selected_target = None"""
 
        # Manejo de errores
        if len(self._selected_features) == 0:  # Si no ha elegido ningun feature
            messagebox.showerror("Error", "Debes seleccionar al menos una columna de entrada (feature).")
        elif not self._selected_target:  # Si no ha elegido ningun target
            messagebox.showerror("Error", "Debes seleccionar una columna de salida (target).")
        else:  # Si todo es correcto, muestra las elecciones por pantalla
            f_cols = ', '.join(col for col in self._selected_features)  # Forma bonita de imprimirlos
            t_col = ', '.join(col for col in self._selected_target)
            messagebox.showinfo("Éxito", f"Columnas de entrada seleccionadas: {f_cols}\nColumna de salida seleccionada: {t_col}")


    def show_nan_count(self):
        """Muestra cuántos valores NaN hay en las columnas seleccionadas por el usuario (features y target)."""
        if not self._selected_features or not self._selected_target:
            messagebox.showerror("Error", "Debes seleccionar las columnas primero.")
            return
        
        # Combinar las columnas seleccionadas en features y target
        selected_columns = self._selected_features + self._selected_target
        
        # Contamos los NaN solo en las columnas seleccionadas
        nan_count = self._df[selected_columns].isnull().sum()
        nan_columns = nan_count[nan_count > 0]

        if not nan_columns.empty:
            message = "Valores inexistentes detectados en las siguientes columnas:\n"
            for col, count in nan_columns.items():
                message += f"- {col}: {count} valores faltantes\n"
            messagebox.showinfo("Valores Inexistentes", message)
            
            # Abrir la ventana para manejar NaN solo si no se ha abierto antes
            if not hasattr(self, 'nan_window') or not self.nan_window.winfo_exists():
                self.open_nan_selection_window()
        else:
            messagebox.showinfo("Valores Inexistentes", "No se detectaron valores inexistentes en las columnas seleccionadas.")


    def open_nan_selection_window(self):
        """Abre una ventana para seleccionar el manejo de valores inexistentes."""
        self.nan_window = tk.Toplevel(self._frame)  # Ventana nueva
        self.nan_window.title("Manejo de Datos Inexistentes")
        self.nan_window.geometry("300x200")
 
        label = tk.Label(self.nan_window, text="Selecciona el método para manejar NaN:")
        label.pack(pady=10)
 
        self.method_var = tk.StringVar()
        
        # Desplegable para elegir el método de manejo de valores inexistentes
        self.method_dropdown = ttk.Combobox(self.nan_window, textvariable=self.method_var, state="readonly", width=30)
        # Asigna los valores a elegir
        self.method_dropdown['values'] = ("Eliminar Filas", "Rellenar con Media", "Rellenar con Mediana", "Rellenar con Valor Constante")
        self.method_dropdown.pack(pady=10)
 
        # Caja para escribir texto ?
        self.valor_entrada_cte = tk.Entry(self.nan_window, width=20)
        self.valor_entrada_cte.pack(pady=5)
        self.valor_entrada_cte.pack_forget()  # La oculta
 
        # Evento cuando se elija una opción
        self.method_dropdown.bind("<<ComboboxSelected>>", self.toggle_cte_entry)
 
        # Botón para aplicar la elección
        apply_button = tk.Button(self.nan_window, text="Aplicar", command=self.apply_nan_handling)
        apply_button.pack(pady=10)

    def toggle_cte_entry(self, event):
        """Muestra u oculta la entrada de valor constante."""
        if self.method_var.get() == "Rellenar con Valor Constante":
            self.valor_entrada_cte.pack()
        else:
            self.valor_entrada_cte.pack_forget()
 
    def apply_nan_handling(self):
        """Aplica el método de manejo de NaN seleccionado a las columnas (features y target)."""
        method = self.method_var.get()

        if not method:
            messagebox.showwarning("Advertencia", "Debes seleccionar un método para manejar los valores inexistentes.")
            return

        # Combina las features y el target en una lista de columnas seleccionadas
        columns_to_handle = self.selected_features + self.selected_target

        if method == "Eliminar Filas":
            self._df.dropna(subset=columns_to_handle, inplace=True)
        elif method == "Rellenar con Media":
            self._df[columns_to_handle] = self._df[columns_to_handle].fillna(self._df[columns_to_handle].mean())
        elif method == "Rellenar con Mediana":
            self._df[columns_to_handle] = self._df[columns_to_handle].fillna(self._df[columns_to_handle].median())
        elif method == "Rellenar con Valor Constante":
            try:
                constant_value = float(self.valor_entrada_cte.get())
                self._df[columns_to_handle] = self._df[columns_to_handle].fillna(constant_value)
            except ValueError:
                messagebox.showerror("Error", "Debes introducir un valor numérico válido.")
                return

        self.nan_window.destroy()
        messagebox.showinfo("Éxito", "El manejo de datos inexistentes se ha aplicado correctamente.")


# Inicialización de la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Selector de Columnas")
    root.geometry("600x400")
 
    # Crear un DataFrame de ejemplo
    data = {
        "Columna1": [1, 2, None, 4],
        "Columna2": [None, 1, 2, 3],
        "Columna3": [1, None, None, 4],
        "Columna4": [5, 6, 7, 8],
    }
    df = pd.DataFrame(data)
    dataset_columns = df.columns.tolist()
 
    main_frame = tk.Frame(root)
    main_frame.pack(expand=True, fill='both')
 
    column_selector = ColumnSelector(main_frame, dataset_columns, df)
 
    root.mainloop()