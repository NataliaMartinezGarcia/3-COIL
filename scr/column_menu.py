import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from nan_handler import NaNHandler, ConstantValueError
from linear_regression_interface import LinearRegressionInterface

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
        features_frame = tk.Frame(self._frame, width=290, height=170,bg = '#d0d7f2')
        features_frame.place(relx=0.03, rely=0.25, relwidth=0.5, anchor="w")

        # Etiqueta
        label = tk.Label(features_frame, text="Select an input column (feature):", fg = '#4d598a', bg = '#d0d7f2',
                                font= ("DejaVu Sans Mono",10, 'bold'),width = 35)
        label.place(relx=0.5, rely=0.1, anchor="center")
        
        # Contenedor que mantiene juntos el listbox y la scrollbar
        container_frame = tk.Frame(features_frame)
        container_frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.5, anchor="center")

        # Crear el Listbox y colocarlo en el lado izquierdo del container_frame
        self._feature_listbox = tk.Listbox(container_frame, selectmode=tk.SINGLE, height=5, exportselection=False)
        self._feature_listbox.pack(side="left", fill="both", expand=True)
        self._feature_listbox.bind("<<ListboxSelect>>", self._manager.on_select)

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
        target_frame = tk.Frame(self._frame, width=280, height=170, bg = '#d0d7f2')
        target_frame.place(relx=0.97, rely=0.25, relwidth=0.5, anchor="e")

        label = tk.Label(target_frame, text="Select an output column (target):", fg = '#4d598a', bg = '#d0d7f2',
                                font= ("DejaVu Sans Mono",10, 'bold'),width = 35)
        label.place(relx=0.5, rely=0.1, anchor="center")

        # Contenedor que mantiene juntos el listbox y la scrollbar
        container_frame = tk.Frame(target_frame)
        container_frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.5, anchor="center")

        self._target_listbox = tk.Listbox(container_frame, selectmode=tk.SINGLE, height=5, exportselection=False)
        self._target_listbox.bind("<<ListboxSelect>>", self._manager.on_select)
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
        confirm_button = tk.Button(self._frame, text="Confirm selection", command=self._manager.confirm_selection,
                                   font=("Arial", 11,'bold'), fg="#FAF8F9", bg = '#6677B8' ,activebackground="#808ec6",
                                   activeforeground="#FAF8F9",cursor="hand2" )
        
        confirm_button.place(relx=0.5, rely=0.45, anchor='center')

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
    toggle_cte_input(event):
        Habilita o deshabilita el campo de entrada para un valor constante basado en el método seleccionado.
    create_apply_button():
        Crea y coloca el botón para aplicar el método seleccionado.
    enable_selector():
        Habilita el selector de métodos.
    disable_selector():
        Deshabilita el selector de métodos y limpia la selección actual.
    """
    # Constante: métodos para tratar los NaN
    METHODS = ("Delete Rows", "Fill with Mean", 
                "Fill with Median", "Fill with a Constant Value")
    
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
        label = tk.Label(self._frame, text="Select a method to handle NaN:", fg = '#4d598a', bg = '#d0d7f2',font= ("DejaVu Sans Mono", 10,'bold'))
        label.place(relx=0.5, rely=0.59, anchor="center")

        self._method_dropdown = ttk.Combobox(self._frame, textvariable=self._method_var, state="disabled", width=30)
        # textvariable=self._method_var: vincula el desplegable a la variable self._method_var
        # El valor seleccionado se actualiza automáticamente en self._method_var.
      
        self._method_dropdown['values'] = ("Delete Rows", "Fill with Mean", "Fill with Median", "Fill with a Constant Value")
        self._method_dropdown.place(relx=0.5, rely=0.67, relwidth=0.5, anchor="center")
        self._method_dropdown.bind("<<ComboboxSelected>>", self.toggle_cte_input)
        
        self._constant_label = tk.Label(self._frame, text="Introduce the constant:", fg = '#4d598a', bg = '#d0d7f2')
        self._constant_value_input = tk.Entry(self._frame, width=10, state="disabled")

        self._constant_value_input.place_forget()  # Ocultarlo inicialmente
        self._constant_label.place_forget()

        separator = tk.Frame(self._frame, bg = '#6677B8', height=3)
        separator.pack(fill = tk.X, side='bottom' )


    def toggle_cte_input(self, event):
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
        
        # Cada vez que cambie la forma de procesado bloquea el botón de regresión
        # para obligarle a pulsar aceptar y usar así la selección más actualizada
        self._manager.disable_regression_button()

        selected_method = self._method_var.get()

        if selected_method == "Fill with a Constant Value": 
            self._constant_label.place(relx=0.45, rely=0.73, anchor="center")
            self._constant_value_input.place(relx=0.6, rely=0.73, anchor="center")
            self._constant_value_input.config(state="normal")
            self._constant_value_input.bind("<KeyRelease>", lambda event: self._manager.disable_regression_button())
        else:
            self._constant_label.place_forget()
            self._constant_value_input.place_forget()  # Ocultarlo inicialment
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
        apply_button = tk.Button(self._frame, text="Apply", command=self._manager.apply_nan_handling, state="disabled",
                                 font=("Arial", 10,'bold'), fg="#FAF8F9", bg = '#6677B8' , activebackground="#808ec6",
                                 activeforeground="#FAF8F9", cursor="hand2" )
        apply_button.place(relx=0.5, rely=0.80, anchor="center")
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

    METHOD_NAMES = ("Delete Rows", "Fill with Mean", 
               "Fill with Median", "Fill with a Constant Value")
    
    def __init__(self, app, frame, columns, df, chart_frame):
        self._app = app  # Solo lo usamos para actualizar la zona de scroll

        self._frame = frame
        self._columns = columns
        self._df = df
        self._new_df = None  # DataFrame donde estarán los datos preprocesados

        self._chart_frame = chart_frame  # Frame donde estará la gráfica

        self._column_menu = ColumnMenu(self._frame, columns, self)
        self._method_menu = MethodMenu(self._frame, self)
        self.create_regression_button()

        # Para que se actualice el área de scroll
        # Hay que llamar a esta función siempre que creemos un widget nuevo
        # (Habrá que llamarla otra vez después de generar la gráfica)
        self._app.scroll_window.update()

        print("df Before pre-processing")
        print(self._df)

        print("new_df Before pre-processing")
        print(self._new_df)

    @property
    def df(self):
        return self._df
    
    @property
    def new_df(self):
        return self._new_df
    
    def on_select(self, event):
        self._method_menu.disable_selector()
        self.disable_regression_button()

    def create_regression_button(self):
        """Crea el botón para iniciar el proceso de creación del modelo de regresión lineal."""
        self._regression_button = tk.Button(self._frame, text="Create Linear Regression Model", 
                                       command=self.create_linear_model,
                                       state = "disabled",  # Empieza deshabilitado
                                       font=("Arial", 10, 'bold'), fg="#FAF8F9", 
                                       bg='#6677B8', activebackground="#808ec6",
                                       activeforeground="#FAF8F9", cursor="hand2")
        self._regression_button.place(relx=0.5, rely=0.93, anchor='center')

    def enable_regression_button(self):
        """Habilita el botón de crear modelo.

        Returns
        -------
        None.
        """
        self._regression_button.config(state="normal")

    def disable_regression_button(self):
        """Deshabilita el botón de crear modelo.

        Returns
        -------
        None.
        """
        self._regression_button.config(state="disabled")

    def confirm_selection(self):
        # Actualiza las variables selected_features y selected_target
        # de ColumnMenu con la selección actual
        self._column_menu.get_selected_columns()

        # Obtiene las selecciones de ColumnMenu
        selected_features = self._column_menu.selected_features
        selected_target = self._column_menu.selected_target

        if len(selected_features) == 0:
            messagebox.showerror("Error", "You must select an input column (feature).")

        elif len(selected_target) == 0:
            messagebox.showerror("Error", "You must select an output column (target).")
        
        else:
            f_cols = ', '.join(selected_features)
            t_col = ', '.join(selected_target)
            success_window = messagebox.showinfo("Success", f"Feature: {f_cols}\nTarget: {t_col}")
            
            if success_window == 'ok':
                # Crea una instancia del objeto NaNHandler después de tener seleccionadas las columnas
                self._nan_handler = NaNHandler(self._df, MenuManager.METHOD_NAMES, 
                                         selected_features + selected_target)
                # Comprobar si hay valores nulos en las columnas seleccionadas
                has_missing, nan_message = self._nan_handler.check_for_nan()
                
                messagebox.showinfo("Non-existent values", nan_message)
                if has_missing:
                    self._method_menu.enable_selector()  # Habilitar el selector si hay valores nulos
                    self.disable_regression_button()  # Lo deshabilita si cambia las columnas
                else:
                    self._method_menu.disable_selector() # Deshabilitar el selector si no hay valores nulos
                    self.enable_regression_button()  # Permite crear el modelo 

    def apply_nan_handling(self):
        method = self._method_menu.method_var.get()
        constant_value = self._method_menu.constant_value_input

        # Estará vacío si no ha introducido nada (porque ha elegido otro método o porque no lo ha introducido cuando toca).
        if constant_value is None or constant_value.strip() == "":
            constant_value = None  # Nos aseguramos de que es None si no ha introducido nada
        else:
            try:
                constant_value = float(constant_value)  # Convertir a float
            except ValueError:
                messagebox.showerror("Error", "The constant value must be a number.")
                return  # Salimos del método si no es un número válido

        try:
            # Aplicamos el preprocesamiento con el método seleccionado
            self._new_df = self._nan_handler.preprocess(method, constant_value)
        except ConstantValueError as e:
            messagebox.showerror("Error", str(e))
            return  # Salimos del método si hay un error

        # Si no hay errores, mostramos éxito y habilitamos el botón de regresión
        print("\ndf After pre-processing")
        print(self._df)

        print("\nnew_df Before pre-processing")
        print(self._new_df)

        messagebox.showinfo("Success", "Non-existent data handling has been successfully applied.")
        self.enable_regression_button()  # Permite crear el modelo

    def create_linear_model(self):
        """Crea el modelo de regresión lineal utilizando las columnas seleccionadas."""
        if len(self._column_menu.selected_features) == 0 or len(self._column_menu.selected_target) == 0:
            messagebox.showerror("Error", "You must select input and output columns before creating the model.")

        # Usar el DataFrame procesado si existe, si no, usar el original
        df_to_use = self._new_df if self._new_df is not None else self._df

        # Obtener la primera feature seleccionada (para regresión simple)
        feature = df_to_use[self._column_menu.selected_features[0]]
        target = df_to_use[self._column_menu.selected_target[0]]

        # Verificar si hay suficientes datos para crear el modelo
        if len(feature) < 2 or len(target) < 2:
            messagebox.showerror("Error", "There isn't enough data to create the regression model.")

        # Mostrar mensaje de éxito y esperar confirmación
        success = messagebox.showinfo("Success", "The linear regression model will be created successfully.\nPress OK to see the results.")
        
        if success == 'ok':
            self.clear_frame(self._chart_frame)  # Lo vaciamos si hay algo

            # Crear el modelo de regresión
            LinearRegressionInterface(self._chart_frame, feature, target)
            self._app.scroll_window.update()  #########
    
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
