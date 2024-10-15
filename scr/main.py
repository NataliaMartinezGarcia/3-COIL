import tkinter as tk 
from tkinter import messagebox, filedialog, ttk  
import pandas as pd 
import sqlite3 

# Función principal que crea la ventana
def ventana():
    ventana = tk.Tk()  # Crea la ventana principal
    ventana.title("Data Explorer")  # Título de la ventana
    ventana.geometry("800x600")  # Tamaño inicial de la ventana

    # Etiqueta principal en la parte superior
    etiqueta = tk.Label(ventana, text="DATA EXPLORER", bg="turquoise", font=("Arial", 16))
    etiqueta.pack(pady=10)  # Añade la etiqueta a la ventana con un margen superior

    # Botón para buscar archivo
    boton_buscar = tk.Button(ventana, text="Presiona para buscar un archivo", font=("Arial", 12), command=buscar_archivo, padx=20, pady=10)
    boton_buscar.pack(pady=10)  # Añade el botón a la ventana con un margen superior

    etiqueta2 = tk.Label(ventana, text = 'Los datos se cargarán en el espacio y la ruta del archivo seleccionado se indicará a seguir' )
    etiqueta2.pack(pady=10)

    # Etiqueta para mostrar la ruta del archivo seleccionado
    global ruta_archivo  # Variable global para almacenar y mostrar la ruta del archivo
    ruta_archivo = tk.StringVar()  # Variable de Tkinter para guardar texto
    etiqueta_ruta = tk.Label(ventana, textvariable=ruta_archivo, bg="lightgray", wraplength=600)
    etiqueta_ruta.pack(pady=5)  # Añade la etiqueta a la ventana para mostrar la ruta del archivo seleccionado

    # Frame para la tabla de datos con scrollbars
    global frame_tabla, tabla, scroll_x, scroll_y
    frame_tabla = tk.Frame(ventana)  # Crea un contenedor para la tabla y los scrollbars
    frame_tabla.pack(fill=tk.BOTH, expand=True)  # El frame ocupará todo el espacio disponible en la ventana

    # Scrollbars horizontales y verticales para la tabla
    scroll_x = tk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL)  # Scroll horizontal
    scroll_y = tk.Scrollbar(frame_tabla, orient=tk.VERTICAL)  # Scroll vertical

    # Tabla para mostrar los datos
    tabla = ttk.Treeview(frame_tabla, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # La tabla se expandirá para llenar el frame

    # Configuración de los scrollbars
    scroll_x.config(command=tabla.xview)  # Conecta el scroll horizontal a la tabla
    scroll_y.config(command=tabla.yview)  # Conecta el scroll vertical a la tabla

    # Añade los scrollbars al frame
    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)  # Posiciona el scroll horizontal abajo de la tabla
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)  # Posiciona el scroll vertical a la derecha de la tabla

    return ventana  # Devuelve la ventana principal

# función para abrir el explorador de archivos y cargar datasets
def buscar_archivo():
    # Abre un cuadro de diálogo para seleccionar archivos con los tipos especificados
    archivo = filedialog.askopenfilename(
        title="Buscar archivo",
        filetypes=[("Archivos compatibles(csv,Excel,SQL)", "*.csv;*.xlsx;*.xls;*.sqlite;*.db")],  # Un solo filtro que permite ver todos los tipos compatibles
        defaultextension=".csv"
    )
    if archivo:  # Si se ha seleccionado un archivo
        ruta_archivo.set(f"Archivo seleccionado: {archivo}")  # Actualiza la etiqueta con la ruta del archivo seleccionado
        try:
            # Carga el archivo según su tipo (CSV, Excel o SQLite)
            if archivo.endswith('.csv'):
                df = pd.read_csv(archivo)  # Lee archivos CSV con pandas
            elif archivo.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(archivo)  # Lee archivos Excel con pandas
            elif archivo.endswith(('.sqlite', '.db')):
                conn = sqlite3.connect(archivo)  # Conecta a la base de datos SQLite
                query = "SELECT name FROM sqlite_master WHERE type='table';"
                tables = pd.read_sql(query, conn)  # Consulta para obtener las tablas de la base de datos
                if not tables.empty:
                    table_name = tables.iloc[0, 0]  # Usa la primera tabla encontrada en la base de datos
                    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)  # Carga los datos de la tabla
                else:
                    messagebox.showwarning("Advertencia", "La base de datos no contiene tablas.")  # Mensaje de advertencia si no hay tablas
                    return
            mostrar_datos(df)  # Muestra los datos cargados en la tabla
        except Exception as e:  # Maneja cualquier error durante la carga del archivo
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")  # Mensaje de error
    else:
        messagebox.showwarning("Advertencia", "No has seleccionado ningún archivo.")  # Mensaje de advertencia si no se selecciona archivo

# Función para mostrar los datos en la tabla
def mostrar_datos(df):
    # Limpiamos la tabla si ya tenía datos
    for widget in tabla.get_children():
        tabla.delete(widget)  # Elimina las filas previas de la tabla

    # Configurar las columnas de la tabla
    tabla["columns"] = list(df.columns)  # Establece las columnas de la tabla a partir del DataFrame
    tabla["show"] = "headings"  # Muestra solo los encabezados de las columnas
    for col in df.columns:
        tabla.heading(col, text=col)  # Establece los encabezados de las columnas
        tabla.column(col, width=100, minwidth=50)  # Ajusta el ancho de cada columna

    # Insertar filas de datos
    for index, row in df.iterrows():  # Itera sobre cada fila del DataFrame
        tabla.insert("", tk.END, values=list(row))  # Inserta cada fila de datos en la tabla


if __name__ == "__main__":
    ventana = ventana()  # Crea la ventana principal
    ventana.mainloop()  # Inicia el bucle principal de la aplicación
