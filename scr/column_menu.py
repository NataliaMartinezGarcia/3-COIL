import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
#import preprocesado 

# Clase que implementa la interfaz para seleccionar columnas de entrada y salida
class ColumnMenu:

    def __init__(self, frame, columns, df):
        self._frame = frame  # Frame donde estarán los desplegables
        self._columns = columns  # Columnas a elegir
        self._df = df  # DataFrame del que se eligen las columnas

        # Variables para almacenar las selecciones
        self._selected_features = []
        self._selected_target = []

        # Estas funciones son simplemente para que no se ponga todo el código en el init
        # Como el create_widgets de las otras clases
        self.create_features_selector()  # Función que crea el selector de features
        self.create_target_selector()  # Función que crea el selector de target
        self.create_confirm_button()  # Función que crea el botón de confirmar
        self.create_nan_selector()

    # Getter para obtener las features desde fuera de la clase
    @property    
    def selected_features(self):
        return self._selected_features
 
    # Getter para obtener el target desde fuera de la clase
    @property    
    def selected_target(self):
        return self._selected_target
    
    def create_features_selector(self):
        """Crea una ListBox para elegir una o varias columnas de entrada o features."""
        features_frame = tk.Frame(self._frame, width=280, height=170)
        features_frame.place(relx=0.03, rely=0.4, relwidth=0.5, anchor="w")
 
        # Etiqueta que indica si se deben elegir 1 o más columnas
        label = tk.Label(features_frame, text = "Selecciona una o varias columnas de entrada (features):", wraplength=270)
        # wraplength=270 para que el texto no se corte con el borde del frame
        label.place(relx=0.5, rely=0.1, relwidth=1, anchor="center")
       
        # Listbox donde se elegirán esas columnas
        self._feature_listbox = tk.Listbox(features_frame, selectmode=tk.MULTIPLE, height=5, exportselection=False)
        # exportselection=False -> para que las selecciones no se borren al interactuar con
        # otro widget que no sea el botón de confirmar

        # Evento que bloquea el desplegable de métodos de preprocesado cada vez que se selecciona una opción
        self._feature_listbox.bind("<<ListboxSelect>>", self.on_target_select)

        # Ahora mismo la listbox está vacía
        # Le metemos las columnas que nos han pasado
        for column in self._columns:
            self._feature_listbox.insert(tk.END, column)
        
        self._feature_listbox.place(relx=0.1, rely=0.46, relwidth=0.75, anchor="w")
 
        # Barra de desplazamiento vertical para cuando haya muchas columnas
        scrollbar = tk.Scrollbar(features_frame, orient="vertical")
        scrollbar.config(command=self._feature_listbox.yview)
        scrollbar.place(relx=0.8, rely=0.46, relheight=0.5, anchor="w")
        self._feature_listbox.config(yscrollcommand=scrollbar.set)

    def create_target_selector(self):
        """Crea un ListBox para elegir la columna de salida o target."""
        
        target_frame = tk.Frame(self._frame, width=280, height=170)
        target_frame.place(relx=0.97, rely=0.4, relwidth=0.5, anchor="e")
 
        # Etiqueta que indica que se debe elegir 1 columna
        label = tk.Label(target_frame, text="Selecciona la columna de salida (target):")
        label.place(relx=0.5, rely=0.1, relwidth=1, anchor="center")
    
        # Listbox donde se dan a elegir las columnas
        self._target_listbox = tk.Listbox(target_frame, selectmode=tk.SINGLE, height=5, exportselection=False)
        self._target_listbox.place(relx=0.1, rely=0.46, relwidth=0.75, anchor="w")
        
        # Evento que bloquea el desplegable de métodos de preprocesado cada vez que se selecciona una opción
        self._target_listbox.bind("<<ListboxSelect>>", self.on_target_select)

        # Barra de desplazamiento vertical para cuando haya muchas columnas
        scrollbar = tk.Scrollbar(target_frame, orient="vertical")
        scrollbar.config(command=self._target_listbox.yview)
        scrollbar.place(relx=0.8, rely=0.46, relheight=0.5, anchor="w")
        self._target_listbox.config(yscrollcommand=scrollbar.set)
 
        # Ahora mismo la listbox está vacía
        # Le metemos las columnas que nos han pasado
        for column in self._columns:
            self._target_listbox.insert(tk.END, column)
    
    def create_confirm_button(self):
        """Botón para confirmar las selecciones."""
        confirm_button = tk.Button(self._frame, text="Confirmar selección", command=self.confirm_selection)
        confirm_button.place(relx=0.5, rely=0.58, anchor='center')

    def confirm_selection(self):
        # Obtiene las features seleccionadas en el listbox
        # Es una lista que tendrá 1 solo elemento si solo se ha elegido 1 (simple)
        # y varios elementos si se ha elegido más de 1 (múltiple)
        self._selected_features = [self._feature_listbox.get(i) for i in self._feature_listbox.curselection()]
 
        # Obtiene el target seleccionado
        self._selected_target = [self._target_listbox.get(i) for i in self._target_listbox.curselection()]

        # Manejo de errores
        if len(self._selected_features) == 0:  # Si no ha elegido ningun feature
            messagebox.showerror("Error", "Debes seleccionar al menos una columna de entrada (feature).")
        elif len(self._selected_target) == 0:  # Si no ha elegido ningun target
            messagebox.showerror("Error", "Debes seleccionar una columna de salida (target).")
        else:  # Si todo es correcto, muestra las elecciones por pantalla
            f_cols = ', '.join(col for col in self._selected_features)  # Forma bonita de imprimirlos
            t_col = ', '.join(col for col in self._selected_target)
            success_window = messagebox.showinfo("Éxito", f"Feature: {f_cols}\nTarget: {t_col}")

            # Después de que el usuario cierre el cuadro de diálogo de éxito, detecta NaN
            if success_window == 'ok':  # Si el usuario cierra la ventana de confirmación
                # Llama a la función para detectar NaN en las columnas seleccionadas
                missing_info = self._df[self._selected_features + self._selected_target].isnull().sum()
                missing_columns = missing_info[missing_info > 0]

                # Actualiza la ventana con la información de NaN
                if not missing_columns.empty:
                    nan_message = "Valores inexistentes detectados en las siguientes columnas:\n"
                    for col, count in missing_columns.items():
                        nan_message += f"- {col}: {count} valores faltantes\n"
                    messagebox.showinfo("Valores Inexistentes", nan_message)
                else:
                    messagebox.showinfo("Valores Inexistentes", "No se detectaron valores inexistentes.")

        self.enable_nan_selector() # Habilita el desplegable
    
    # añadida función para que salga el número de valores nan en las columnas seleccionadas 
    def detectar_nan(self):
        """Detecta y muestra cuántos valores inexistentes hay en el DataFrame."""
        if self.df.empty:  # Verificación para asegurarse de que hay un archivo cargado
            messagebox.showwarning("Advertencia", "Debes seleccionar un archivo primero.")  # Muestra advertencia
            return  # Sale de la función

        missing_info = self.df.isnull().sum()  # Calcula el número de valores inexistentes por columna
        missing_columns = missing_info[missing_info > 0]  # Filtra columnas con valores inexistentes
        
        if not missing_columns.empty:  # Si hay columnas con valores inexistentes
            message = "Valores inexistentes detectados en las siguientes columnas:\n"
            for col, count in missing_columns.items():  # Itera sobre las columnas con valores faltantes
                message += f"- {col}: {count} valores faltantes\n"
            messagebox.showinfo("Valores Inexistentes", message)  # Muestra mensaje con la información
        else:
            messagebox.showinfo("Valores Inexistentes", "No se detectaron valores inexistentes.")  # Mensaje si no hay valores faltantes

    def enable_nan_selector(self):
        self._method_dropdown["state"] = "readonly"

    def disable_nan_selector(self):
        self._method_dropdown["state"] = "disabled"

    def on_feature_select(self, event):
        """Deshabilita el selector de método NaN cuando se selecciona un feature."""
        self.disable_nan_selector()

    def on_target_select(self, event):
        """Deshabilita el selector de método NaN cuando se selecciona un target."""
        self.disable_nan_selector()

    def create_nan_selector(self):
        label = tk.Label(self._frame, text="Selecciona el método para manejar NaN:")
        label.place(relx=0.5, rely=0.7, relwidth=0.5, anchor="center")

        self.method_var = tk.StringVar()

        # Desplegable para elegir el método de manejo de valores inexistentes
        self._method_dropdown = ttk.Combobox(self._frame, textvariable=self.method_var, 
                                            state = "disabled", width=30)

        # Asigna los valores a elegir
        self._method_dropdown['values'] = ("Eliminar Filas", "Rellenar con Media", "Rellenar con Mediana", "Rellenar con Valor Constante")
        self._method_dropdown.place(relx=0.5, rely=0.77, relwidth=0.5, anchor="center")

        # Caja para escribir texto (desaparece al inicio)
        self.valor_entrada_cte = tk.Entry(self._frame, width=20)
        self.valor_entrada_cte.pack(pady=5)
        self.valor_entrada_cte.pack_forget()

        # Evento cuando se elija una opción
        self._method_dropdown.bind("<<ComboboxSelected>>", self.toggle_cte_entry)
 
        # Botón para aplicar la elección, inicialmente deshabilitado
        self.apply_button = tk.Button(self._frame, text="Aplicar", command=self.apply_nan_handling, state="disabled")
        self.apply_button.place(relx=0.5, rely=0.88, anchor="center")
    
    def toggle_cte_entry(self, event):
        """Muestra u oculta la entrada de valor constante y habilita el botón 'Aplicar'."""
        selected_method = self.method_var.get()
        
        # Si el usuario elige "Rellenar con Valor Constante", mostramos la caja de entrada
        if selected_method == "Rellenar con Valor Constante":
            self.valor_entrada_cte.pack()
        else:
            self.valor_entrada_cte.pack_forget()

        # Habilitar el botón de aplicar solo si hay un método seleccionado
        if selected_method:
            self.apply_button.config(state="normal")  # Habilita el botón
        else:
            self.apply_button.config(state="disabled")  # Deshabilita el botón si no hay selección

 
    def apply_nan_handling(self):
        """Aplica el método de manejo de NaN seleccionado a las columnas (features y target)."""
        method = self.method_var.get()

        if not method:
            messagebox.showwarning("Advertencia", "Debes seleccionar un método para manejar los valores inexistentes.")
            return None

        # Combina las features y el target en una lista de columnas seleccionadas
        columns_to_handle = list(set(self._selected_features + self._selected_target))
        print(columns_to_handle)
        
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
        
        messagebox.showinfo("Éxito", "El manejo de datos inexistentes se ha aplicado correctamente.")


#############################################
# Prueba
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Selector de Columnas")
    root.geometry("600x400")
 
    # Crear un DataFrame de ejemplo
    # Crear un DataFrame de ejemplo
    data = {
        "Columna1": [1, 2, None, 4],
        "Columna2": [None, 1, 2, 3],
        "Columna3": [1, None, None, 4],
        "Columna4": [5, 6, 7, 8],
        "Columna5": [5, 6, 7, 8],
        "Columna6": [5, 6, 7, 8],
        "Columna7": [5, 6, None, 8],
        "Columna8": [5, 6, 7, 8],
        "Columna9": [5, 6, 7, 8],
        "Columna10": [5, 6, 7, 8]
    }
    df = pd.DataFrame(data)
    dataset_columns = df.columns.tolist()
 
    main_frame = tk.Frame(root)
    main_frame.pack(expand=True, fill='both')
 
    column_selector = ColumnMenu(main_frame, dataset_columns, df)
 
    root.mainloop()
