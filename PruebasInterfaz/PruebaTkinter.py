# documentación -> https://docs.python.org/3/library/tk.html

import tkinter as tk 
from tkinter import messagebox #para que nos salgan ventanas nuevas al presionar botones


# CREACIÓN DE VENTANA INICIAL

# creamos ventana inicial y luego le vamos añadiendo cosas
def ventana():
    ventana = tk.Tk() #para crear la ventana: tk.Tk
    ventana.title("Ejemplo de Tkinter")#para añadir el título: .title 
    ventana.geometry("400x150")# para redimensionar nuestra ventana: .geometry

    # para crear una etiqueta en nuestra ventana: tk.Label
    # parámetro 1: donde va colocada la etiqueta. 
    # parámetro 2: texto que lleva dicha estiqueta (text = "")
    # parámetro 3: color de fondo de texto si nos apetece (bg = "colour")
    etiqueta = tk.Label(ventana, text = "PRUEBA TKINTER", bg = "turquoise") #esto áun no aparece en pantalla 

    #para que aparezca la etiqueta en nuestra ventana: .pack (+ fill o side si queremos estirarlo o cambiarlo de sitio)
    etiqueta.pack()

    # side cambia donde está colocada la etiqueta en la ventana 
    # etiqueta.pack(side = tk.BOTTOM)
    # etiqueta.pack(side = tk.RIGHT)
    # etiqueta.pack(side = tk.LEFT)
    
    # fill estira la etiqueta
    # etiqueta.pack(fill = tk.X)
    # etiqueta.pack(fill = tk.Y, expand = True) si queremos estirarlo verticalmente, añadimos el expand = True 
    # etiqueta.pack(fill = tk.BOTH, expand = True)

    # para crear los botones: tk.Button
    boton1 = tk.Button(ventana, text = 'Presiona para ver mensaje', command = mensaje) #command + función sin paréntesis = funciona el botón 
    # boton = tk.Button(ventana, text = 'Presiona', padx = 20, pady = 10) # padx y pady cambian el tamaño del botón 
    boton1.pack(pady = 10) # el pady en este caso añade una separación entre la etiqueta y el botón

    boton2 = tk.Button(ventana, text = "Presiona para insertar datos", command = obtener_datos)
    boton2.pack(pady = 10)

    return ventana


# PARA DAR FUNCIONALIDAD A LOS BOTONES 
# función para que aparezca un mensaje en otra ventana al presional el bottón 
def mensaje():
    messagebox.showinfo("Mensaje", "¡Has presionado el botón!")
    
# función que crea una nueva ventana para insertar los datos
def obtener_datos():
    nueva_ventana = tk.Toplevel()  # .Toplevel crea una ventana secundaria. 
    nueva_ventana.title("Insertar Datos")
    nueva_ventana.geometry("300x200")
    
    # Etiqueta y campo de entrada para el nombre
    etiqueta_nombre = tk.Label(nueva_ventana, text="Nombre completo:")
    etiqueta_nombre.pack(pady=5)
    nombre_entry = tk.Entry(nueva_ventana) #.Entry permite al usuario insertar el dato  
    nombre_entry.pack(pady=5)
    
    # Etiqueta y campo de entrada para la edad
    etiqueta_edad = tk.Label(nueva_ventana, text="Edad:")
    etiqueta_edad.pack(pady=5)
    edad_entry = tk.Entry(nueva_ventana)
    edad_entry.pack(pady=5)

     # Botón para insertar los datos
    boton_insertar = tk.Button(nueva_ventana, text="Insertar", command=lambda: mostrar_datos(nombre_entry, edad_entry, nueva_ventana))
    boton_insertar.pack(pady=20)

# función para obtener los datos en la nueva ventana
def mostrar_datos(nombre_entry, edad_entry, nueva_ventana):
    nombre = nombre_entry.get()
    edad = edad_entry.get()
    
    if nombre and edad: #verifica si los campos tienen agún valor 
        messagebox.showinfo("Datos insertados", f"Nombre: {nombre}\nEdad: {edad}")
        nueva_ventana.destroy()  # Cierra la ventana de datos después de insertar
    else:
        messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.") 


if __name__ == "__main__":
    ventana = ventana()
    # esto SIEMPRE hay que ponerlo al final para que la app funcione (estructura: primera_ventana.mainloop())
    ventana.mainloop()

