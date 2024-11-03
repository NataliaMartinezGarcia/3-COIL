import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from nan_handler import NaNHandler
from linear_regression import LinearRegression

# Clase que implementa la interfaz para seleccionar columnas de entrada y salida
class ColumnMenu:
    """Interfaz gráfica para seleccionar columnas de entrada y salida de un DataFrame.
    
    Esta clase permite al usuario seleccionar múltiples columnas de entrada ("features") 
    y una columna de salida ("target") en una ventana de Tkinter.
    
    Attributes
    ----------
    _frame : tk.Frame
        Frame principal de la interfaz gráfica donde se colocarán los widgets.
    _columns : list
        Lista de nombres de columnas disponibles para seleccionar.
    _manager : object
        Objeto controlador que maneja la lógica de selección y confirmación.
    _selected_features : list
        Lista de columnas seleccionadas como features.
    _selected_target : list
        Columna seleccionada como target.
    
    Methods
    -------
    add_scrollbar_to_listbox(listbox, container_frame):
        Añade una scrollbar a un Listbox dentro de un contenedor específico.
    create_features_selector():
        Crea el selector de columnas de entrada con un Listbox y scrollbar.
    create_target_selector():
        Crea el selector de columna de salida con un Listbox y scrollbar.
    create_confirm_button():
        Crea un botón que confirma la selección de columnas.
    get_selected_columns():
        Guarda las columnas seleccionadas de entrada y salida en las variables correspondientes.
    """
    def __init__(self, frame, columns, manager):
        """
        Inicializa el menú de selección de columnas.
        
        :param frame: Frame padre donde se ubicarán los widgets.
        :param columns: Lista de nombres de columnas del DataFrame.
        :param manager: Objeto del manager que controla la lógica de selección y confirmación.
        """

        self._frame = frame
        self._columns = columns
        self._manager = manager
        self._selected_features = []
        self._selected_target = []

        self.create_features_selector()
        self.create_target_selector()
        self.create_confirm_button()

    @property
    def selected_features(self):
        """Obtiene la lista de columnas seleccionadas como features.
        
        Returns
        -------
        list
            Lista de nombres de las columnas seleccionadas como features.
        """
        return self._selected_features

    @property
    def selected_target(self):
        """Obtiene la columna seleccionada como target.
        
        Returns
        -------
        list
            Lista que contiene el nombre de la columna seleccionada como target.
        """
        return self._selected_target

    def add_scrollbar_to_listbox(self, listbox, container_frame):
        """Añade una scrollbar vertical a un Listbox dentro de un contenedor específico.
        
        Parameters
        ----------
        listbox : tk.Listbox
            Listbox al que se le añadirá la scrollbar.
        container_frame : tk.Frame
            Frame que contiene el Listbox y donde se ubicará la scrollbar.
        
        Returns
        -------
        None.
        """
        # Crear y colocar la scrollbar vertical
        scrollbar = tk.Scrollbar(container_frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

    def create_features_selector(self):
        """Crea el selector de columnas de entrada (features).
        
        Incluye un contenedor con una etiqueta descriptiva, un Listbox de selección múltiple 
        y una scrollbar vertical.
        
        Returns
        -------
        None.
        """
        # Frame principal que contiene la etiqueta y el container_frame con el listbox y scrollbar
        features_frame = tk.Frame(self._frame, width=290, height=170)
        features_frame.place(relx=0.03, rely=0.4, relwidth=0.5, anchor="w")

        # Etiqueta
        label = tk.Label(features_frame, text="Selecciona una o varias columnas de entrada (features):", wraplength=270)
        label.place(relx=0.5, rely=0.1, relwidth=1, anchor="center")
        
        # Contenedor que mantiene juntos el listbox y la scrollbar
        container_frame = tk.Frame(features_frame)
        container_frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.5, anchor="center")

        # Crear el Listbox y colocarlo en el lado izquierdo del container_frame
        self._feature_listbox = tk.Listbox(container_frame, selectmode=tk.SINGLE, height=5, exportselection=False)
        self._feature_listbox.pack(side="left", fill="both", expand=True)
        self._feature_listbox.bind("<<ListboxSelect>>", self._manager.on_column_select)

        for column in self._columns:
            self._feature_listbox.insert(tk.END, column)

        # Llamar a la función para agregar el scrollbar al Listbox
        self.add_scrollbar_to_listbox(self._feature_listbox, container_frame)

    def create_target_selector(self):
        """Crea el selector de columna de salida (target).
        
        Incluye un contenedor con una etiqueta descriptiva, un Listbox de selección única 
        y una scrollbar vertical.
        
        Returns
        -------
        None.
        """
        target_frame = tk.Frame(self._frame, width=280, height=170)
        target_frame.place(relx=0.97, rely=0.4, relwidth=0.5, anchor="e")

        label = tk.Label(target_frame, text="Selecciona la columna de salida (target):")
        label.place(relx=0.5, rely=0.1, relwidth=1, anchor="center")

        # Contenedor que mantiene juntos el listbox y la scrollbar
        container_frame = tk.Frame(target_frame)
        container_frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.5, anchor="center")

        self._target_listbox = tk.Listbox(container_frame, selectmode=tk.SINGLE, height=5, exportselection=False)
        self._target_listbox.bind("<<ListboxSelect>>", self._manager.on_column_select)
        # Usamos pack para que se expanda dentro del frame que lo empaqueta con el scrollbar
        self._target_listbox.pack(side="left", fill="both", expand=True)

        for column in self._columns:
            self._target_listbox.insert(tk.END, column)

        # Llamar a la función para agregar el scrollbar al Listbox
        self.add_scrollbar_to_listbox(self._target_listbox, container_frame)

    def create_confirm_button(self):
        """Crea un botón que permite confirmar la selección de columnas.
        
        El botón activa el método 'confirm_selection' del manager para procesar 
        las columnas seleccionadas.
        
        Returns
        -------
        None.
        """
        confirm_button = tk.Button(self._frame, text="Confirmar selección", command=self._manager.confirm_selection,
                                   font=("Arial", 12,'bold'), fg="#FAF8F9", bg = '#6677B8' ,activebackground="#808ec6",
                                   activeforeground="#FAF8F9",cursor="hand2" )
        
        confirm_button.place(relx=0.5, rely=0.58, anchor='center')

    def get_selected_columns(self):
        """Guarda las columnas seleccionadas en los Listbox de entrada y salida.
        
        Almacena las columnas seleccionadas de entrada y salida en las variables 
        '_selected_features' y '_selected_target', respectivamente.
        
        Returns
        -------
        None.
        """
        self._selected_features = [self._feature_listbox.get(i) for i in self._feature_listbox.curselection()]
        self._selected_target = [self._target_listbox.get(i) for i in self._target_listbox.curselection()]

class MethodMenu:
    """Clase para manejar la selección de métodos para tratar los valores NaN en datos.

    Attributes
    ----------
    _frame : tk.Frame
        El marco en el que se colocan los componentes de la interfaz gráfica.
    _manager : objeto
        El administrador que gestiona la lógica relacionada con el tratamiento de datos.
    _method_var : tk.StringVar
        Variable que contiene el método seleccionado para manejar los NaN.

    Methods
    -------
    create_nan_selector():
        Crea y coloca el selector de métodos en la interfaz gráfica.
    toggle_cte_entry(event):
        Habilita o deshabilita el campo de entrada para un valor constante basado en el método seleccionado.
    create_apply_button():
        Crea y coloca el botón para aplicar el método seleccionado.
    enable_selector():
        Habilita el selector de métodos.
    disable_selector():
        Deshabilita el selector de métodos y limpia la selección actual.
    """
    # Constante: métodos para tratar los NaN
    METHODS = ("Eliminar Filas", "Rellenar con Media", 
                "Rellenar con Mediana", "Rellenar con Valor Constante")
    
    def __init__(self, frame, manager):
        """Inicializa la clase MethodMenu.

        Parameters
        ----------
        frame : tk.Frame
            El marco en el que se colocarán los componentes de la interfaz gráfica.
        manager : objeto
            El administrador que gestiona la lógica relacionada con el tratamiento de datos.
        Returns
        -------
        None.
        """
        self._frame = frame
        self._manager = manager
        self._method_var = tk.StringVar()

        self.create_nan_selector()
        self._apply_button = self.create_apply_button()

    @property 
    def method_var(self):
        """Devuelve el método seleccionado.

        Returns
        -------
        tk.StringVar
            Variable que contiene el método seleccionado para manejar NaN.
        """
        return self._method_var
    
    @property
    def constant_value_input(self):
        return self._constant_value_input.get()
    
    def create_nan_selector(self):
        """Crea y coloca el selector de métodos en la interfaz gráfica.

        Este método crea una etiqueta y un Combobox para seleccionar el método
        de manejo de NaN, así como un campo de entrada para un valor constante
        si es necesario.

        Returns
        -------
        None.
        """
        label = tk.Label(self._frame, text="Selecciona el método para manejar NaN:")
        label.place(relx=0.5, rely=0.7, relwidth=0.5, anchor="center")

        self._method_dropdown = ttk.Combobox(self._frame, textvariable=self._method_var, state="disabled", width=30)
        # textvariable=self._method_var: vincula el desplegable a la variable self._method_var
        # El valor seleccionado se actualiza automáticamente en self._method_var.
        # Al momento de crearlo está
        self._method_dropdown['values'] = ("Eliminar Filas", "Rellenar con Media", "Rellenar con Mediana", "Rellenar con Valor Constante")
        self._method_dropdown.place(relx=0.5, rely=0.77, relwidth=0.5, anchor="center")
        self._method_dropdown.bind("<<ComboboxSelected>>", self.toggle_cte_entry)

        self._constant_value_input = tk.Entry(self._frame, width=20, state="disabled")
        self._constant_value_input.place(relx=0.5, rely=0.83, relwidth=0.5, anchor="center")

    def toggle_cte_entry(self, event):
        """Habilita o deshabilita el campo de entrada para un valor constante
        basado en el método seleccionado.

        Parameters
        ----------
        event : Event
            Evento de selección en el Combobox.

        Returns
        -------
        None.
        """
        selected_method = self._method_var.get()
        if selected_method == "Rellenar con Valor Constante":
            self._constant_value_input.config(state="normal")
        else:
            self._constant_value_input.delete(0, "end")
            self._constant_value_input.config(state="disabled")

        if selected_method:
            self._apply_button.config(state="normal")
        else:
            self._apply_button.config(state="disabled")

    def create_apply_button(self):
        """Crea y coloca el botón para aplicar el método seleccionado.

        Returns
        -------
        tk.Button
            El botón creado para aplicar el manejo de NaN.
        """
        apply_button = tk.Button(self._frame, text="Aplicar", command=self._manager.apply_nan_handling, state="disabled",
                                 font=("Arial", 12,'bold'), fg="#FAF8F9", bg = '#6677B8' , activebackground="#808ec6",
                                 activeforeground="#FAF8F9", cursor="hand2" )
        apply_button.place(relx=0.5, rely=0.93, anchor="center")
        return apply_button

    def enable_selector(self):
        """Habilita el selector de métodos.

        Returns
        -------
        None.
        """
        self._method_dropdown["state"] = "readonly"

    def disable_selector(self):
        """Deshabilita el selector de métodos y limpia la selección actual.

        Returns
        -------
        None.
        """
        self._method_var.set("")  # Limpia el valor seleccionado
        self._method_dropdown["state"] = "disabled"

    def display_nan_message(self, message):
        """Muestra un mensaje sobre los valores inexistentes.
        
        Parameters
        ----------
        message : str
            El mensaje a mostrar en el label.

        Returns
        -------
        None.
        """
        self._message_label.config(text=message)

    def clear_nan_message(self):
        """Limpia el mensaje sobre valores inexistentes.
        
        Returns
        -------
        None.
        """
        self._message_label.config(text="")

class MenuManager:

    METHOD_NAMES = ("Eliminar Filas", "Rellenar con Media", 
               "Rellenar con Mediana", "Rellenar con Valor Constante")
    
    def __init__(self, frame, columns, df):
        self._frame = frame
        self._columns = columns
        self._df = df
        self._new_df = None  # DataFrame donde estarán los datos preprocesados

        self._column_menu = ColumnMenu(frame, columns, self)
        self._method_menu = MethodMenu(frame, self)

        # Botón para crear modelo de regresión lineal
        self.create_regression_button()

        print("df Antes del preprocesado")
        print(self._df)

        print("new_df Antes del preprocesado")
        print(self._new_df)

    @property
    def df(self):
        return self._df
    
    @property
    def new_df(self):
        return self._new_df
    
    def on_column_select(self, event):
        self._method_menu.disable_selector()

    def confirm_selection(self):
        # Actualiza las variables selected_features y selected_target
        # de ColumnMenu con la selección actual
        self._column_menu.get_selected_columns()

        # Obtiene las selecciones de ColumnMenu
        selected_features = self._column_menu.selected_features
        selected_target = self._column_menu.selected_target

        if len(selected_features) == 0:
            messagebox.showerror("Error", "Debes seleccionar al menos una columna de entrada (feature).")

        elif len(selected_target) == 0:
            messagebox.showerror("Error", "Debes seleccionar una columna de salida (target).")
        
        else:
            f_cols = ', '.join(selected_features)
            t_col = ', '.join(selected_target)
            success_window = messagebox.showinfo("Éxito", f"Feature: {f_cols}\nTarget: {t_col}")
            
            if success_window == 'ok':
                # Crea una instancia del objeto NaNHandler después de tener seleccionadas las columnas
                self._nan_handler = NaNHandler(self._df, MenuManager.METHOD_NAMES, 
                                         selected_features + selected_target)
                # Comprobar si hay valores nulos en las columnas seleccionadas
                has_missing, nan_message = self._nan_handler.check_for_nan()
                
                messagebox.showinfo("Valores Inexistentes", nan_message)
                if has_missing:
                    self._method_menu.enable_selector()  # Habilitar el selector si hay valores nulos
                else:
                    self._method_menu.disable_selector()  # Deshabilitar el selector si no hay valores nulos

    def apply_nan_handling(self):
        method = self._method_menu.method_var.get()
        
        constant_value = self._method_menu.constant_value_input
        # Estará vacío si no ha introducido nada (porque ha elegido otro método o porque no lo ha introducido cuando toca.)
        if constant_value is None or constant_value.strip() == "":
            constant_value = None # Nos aseguramos de que es None si no ha introducido nada 
        else:
            float(constant_value)

        self._new_df = self._nan_handler.preprocess(method, constant_value)

        print("\ndf Despues del preprocesado")
        print(self._df)

        print("\nnew_df Despues del preprocesado")
        print(self._new_df)

        messagebox.showinfo("Éxito", "El manejo de datos inexistentes se ha aplicado correctamente.")


    def create_regression_button(self):
        """Crea el botón para iniciar el proceso de creación del modelo de regresión lineal."""
        regression_button = tk.Button(self._frame, text="Crear Modelo de Regresión Lineal", 
                                       command=self.create_linear_model,
                                       font=("Arial", 12, 'bold'), fg="#FAF8F9", 
                                       bg='#6677B8', activebackground="#808ec6",
                                       activeforeground="#FAF8F9", cursor="hand2")
        regression_button.place(relx=0.5, rely=0.95, anchor='center')
    
    def create_regression_button(self):
        """Crea el botón para iniciar el proceso de creación del modelo de regresión lineal."""
        regression_button = tk.Button(self._frame, text="Crear Modelo de Regresión Lineal", 
                                    command=self.create_linear_model,
                                    font=("Arial", 12, 'bold'), fg="#FAF8F9", 
                                    bg='#6677B8', activebackground="#808ec6",
                                    activeforeground="#FAF8F9", cursor="hand2")
        regression_button.place(relx=0.5, rely=0.95, anchor='center')

    def create_linear_model(self):
        """Crea el modelo de regresión lineal utilizando las columnas seleccionadas."""
        if len(self._column_menu.selected_features) == 0 or len(self._column_menu.selected_target) == 0:
            messagebox.showerror("Error", "Debes seleccionar columnas de entrada y salida antes de crear el modelo.")
            return

        # Usar el DataFrame procesado si existe, si no, usar el original
        df_to_use = self._new_df if self._new_df is not None else self._df

        # Obtener la primera feature seleccionada (para regresión simple)
        feature = df_to_use[self._column_menu.selected_features[0]]
        target = df_to_use[self._column_menu.selected_target[0]]

        # Verificar si hay suficientes datos para crear el modelo
        if len(feature) < 2 or len(target) < 2:
            messagebox.showerror("Error", "No hay suficientes datos para crear el modelo de regresión.")
            return

        # Mostrar mensaje de éxito y esperar confirmación
        success = messagebox.showinfo("Éxito", "El modelo de regresión lineal se creará correctamente.\nPresione Aceptar para ver los resultados.")
        
        if success == 'ok':
            # Crear nueva ventana para el modelo de regresión
            regression_window = tk.Toplevel()
            regression_window.title("Resultados del Modelo de Regresión Lineal")
            regression_window.geometry("500x200")

            # Crear etiquetas para mostrar resultados
            output_labels = []
            for i in range(3):
                label = tk.Label(regression_window, text="", wraplength=400)
                label.pack(pady=5)
                output_labels.append(label)

            # Crear el modelo de regresión
            LinearRegression(feature, target, output_labels)

                
#############################################
# Prueba
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Selector de Columnas")
    root.geometry("600x400")

        # Cargar datos en un DataFrame de ejemplo
    data = {
        "Columna1": [1, 2, None, 4],
        "Columna2": [None, 1, 2, 3],
        "Columna3": [1, None, None, 4],
        "Columna4": [5, 6, 7, 8],
        "Columna5": [5, 6, 7, 8],
        "Columna6": [5, 6, 7, 8]
    }
    df = pd.DataFrame(data)
    columns = df.columns.tolist()  # Lista de nombres de columnas

    # Crear un marco para contener los menús
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Instanciar el gestor de menús, pasando el marco, columnas y el DataFrame
    menu_manager = MenuManager(frame, columns, df)

    # Ejecutar la aplicación
    root.mainloop()