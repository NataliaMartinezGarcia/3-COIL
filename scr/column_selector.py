import tkinter as tk
from tkinter import messagebox, ttk

# Clase que implementa la interfaz para seleccionar columnas de entrada y salida
class ColumnSelector:
    # Tipos de regresión
    SIMPLE = "Simple"
    MULTIPLE = "Múltiple"
    SIMPLE_LABEL = "Selecciona la columna de entrada (feature):"
    MULTIPLE_LABEL = "Selecciona las columnas de entrada (features):"

    def __init__(self, frame, column):
        self._frame = frame
        self._columns = column  # DataFrame

        # Tipos de regresión a elegir por el usuario
        self._regression_types = [ColumnSelector.SIMPLE, ColumnSelector.MULTIPLE]
        # Por defecto el tipo de regresión es simple
        self._selected_regression_type = self._regression_types[0] 

        self._regression_type_label = tk.StringVar()  # Etiqueta que se actualiza
        self._regression_type_label.set(ColumnSelector.SIMPLE_LABEL)

        # Variables para almacenar las selecciones
        self._selected_features = []
        self._selected_target = None

        self.create_regression_selector()
        self.create_features_selector()
        self.create_target_selector()
        self.create_confirm_button()

    @property    
    def selected_features(self):
        return self._selected_features

    @property    
    def selected_target(self):
        return self._selected_target
    
    def create_regression_selector(self):
        """Crea un desplegable para elegir el tipo de regresión lineal."""

        # Label para seleccionar el tipo de regresión
        tk.Label(self._frame, text="Tipo de regresión:").pack(side='top', padx=5, pady=5)

        # Combobox para seleccionar entre regresión simple o múltiple
        self._regression_type_combobox = ttk.Combobox(self._frame, values=self._regression_types, state="readonly")
        self._regression_type_combobox.pack(side='top', padx=5, pady=5)
        self._regression_type_combobox.set(self._regression_types[0])  # Valor predeterminado

        # Cada vez que ocurra un evento (que el usuario elija una opción en el desplegable), se actualiza
        self._regression_type_combobox.bind("<<ComboboxSelected>>", self.update_regression_type)

    def update_regression_type(self, event=None):
        """Actualizar el modo de selección en el Listbox según el tipo de regresión seleccionado."""
        self._selected_regression_type = self._regression_type_combobox.get()  # Obtener el tipo de regresión seleccionado

        # Cambiar el modo de selección del Listbox
        if self._selected_regression_type == self._regression_types[0]:  # Si es simple
            self._feature_listbox.config(selectmode=tk.SINGLE)
        else:  # Si es múltiple
            self._feature_listbox.config(selectmode=tk.MULTIPLE)

        # Limpiar las selecciones anteriores al cambiar el tipo de regresión
        self._feature_listbox.selection_clear(0, tk.END)
        self._selected_features = []  # Reiniciar la lista de selecciones

        # Actualizar la etiqueta
        self.update_features_label()

    def create_features_selector(self):
        """Crea una ListBox para elegir una o varias columnas de entrada o features."""
        # Crear el label inicial según el tipo de regresión
        # Label para seleccionar columnas de entrada
        features_frame = tk.Frame(self._frame, width=180, height=170)
        features_frame.pack(side='left', padx = 10, pady=5)

        # Cambiará dependiendo del tipo de regresión escogido
        tk.Label(features_frame, textvariable=self._regression_type_label).pack(side='top', pady=5, anchor='w', expand = False)
        self.update_features_label()
        
        # Listbox con Scrollbar para seleccionar múltiples columnas de entrada
        self._feature_listbox = tk.Listbox(features_frame, selectmode=tk.SINGLE, height=5, exportselection=False) 
        self._feature_listbox.pack(side='left', fill='y')

        # Scrollbar para el Listbox a la derecha
        scrollbar = tk.Scrollbar(features_frame, orient="vertical")
        scrollbar.config(command=self._feature_listbox.yview)
        scrollbar.pack(side='left', fill='y')  # Pegada a la Listbox
        self._feature_listbox.config(yscrollcommand=scrollbar.set)

        # Agregar columnas al Listbox
        for column in self._columns:
            self._feature_listbox.insert(tk.END, column)

    def update_features_label(self):
        """Actualizar el texto del Label según el tipo de regresión seleccionado."""
    
        if self._selected_regression_type == self._regression_types[0]:  # Si es regresión simple
            self._regression_type_label.set(ColumnSelector.SIMPLE_LABEL)
        else:  # Si es regresión múltiple
            self._regression_type_label.set(ColumnSelector.MULTIPLE_LABEL)

    def create_target_selector(self):
        """Crea un desplegable para elegir la columna de salida o target."""
        # Frame para el selector de salida para mantener su disposición
        target_frame = tk.Frame(self._frame, width=180, height=200)
        target_frame.pack(side='right',padx=10, pady=10, expand=False)
    
        # Label para seleccionar columnas de salida
        tk.Label(target_frame, text="Selecciona la columna de salida (target):").pack(side='top', fill='y')

        col_list = []
        for column in self._columns:
            col_list.append(column)

        # Combobox para seleccionar entre las columnas
        self._target_combobox = ttk.Combobox(target_frame, values=col_list, state="readonly")
        self._target_combobox.pack(side='top', padx=5, pady=5)

    def create_confirm_button(self):
        # Botón de confirmación
        confirm_button = tk.Button(self._frame, text="Confirmar selección", command=self.confirm_selection)
        confirm_button.pack(side='bottom', padx=20, pady=5)  # Usar pady mayor para evitar que esté pegado al final

    def confirm_selection(self):
        """Botón para confirmar las selecciones."""

        # Este método actualiza los datos seleccionados en las variables de instancia
        # Para obtener los datos seleccionados desde otra clase solo tenemos que 
        # llamar al getter de estas variables
        # nombre_objeto.selected_features y nombre_objeto.selected_target

        # Obtener las selecciones de las columnas de entrada
        selected_features_indices = self._feature_listbox.curselection()
        self._selected_features = [self._columns[i] for i in selected_features_indices]
        
        # Obtener la columna de salida
        self._selected_target = self._target_combobox.get()

        # Validar que se haya seleccionado al menos una feature y un target
        if len(self._selected_features) == 0:
            messagebox.showerror("Error", "Debes seleccionar al menos una columna de entrada (feature).")
        elif not self._selected_target:
            messagebox.showerror("Error", "Debes seleccionar una columna de salida (target).")
        else:
            # Confirmación de la selección 
            cols = ', '.join(col for col in self._selected_features) # Para mostrar la selección
            messagebox.showinfo("Éxito", f"Columnas de entrada seleccionadas: {cols}\nColumna de salida seleccionada: {self._selected_target}")

# Ejemplo de uso dentro de un Tkinter Frame
if __name__ == "__main__":
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Selector de Columnas")

    # Definir columnas de ejemplo
    dataset_columns = [f"Columna {i}" for i in range(1, 21)]  # 20 columnas de ejemplo

    # Crear un frame para la interfaz
    main_frame = tk.Frame(root, padx=10, pady=10)
    main_frame.pack()

    # Instanciar la clase ColumnSelector dentro del frame
    column_selector = ColumnSelector(main_frame, dataset_columns)

    # Iniciar la aplicación
    root.mainloop()