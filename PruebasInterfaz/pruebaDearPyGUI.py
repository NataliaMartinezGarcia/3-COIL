import dearpygui.dearpygui as dpg

def ventana():
    # viewport: ventana dentro de la que aparecen el resto de ventanas
    dpg.create_viewport(title='Mi ventana', width=540, height=450)

    # Será la ventana principal dentro de la que configuramos cosas
    # Tenemos que definir más adelante que esta sea ventana principal
    with dpg.window(label="Ejemplo de DearPyGUI", width=540, height=200):

        # Añadir texto rodeado de un rectángulo
        with dpg.drawlist(width=400, height=80, pos = [300, 300]): # drawlist crea un área de dibujo dentro de la ventana
            # pos = [posición en el eje x, posición en el eje y]. [0, 0] sería la esquina superior izquierda
            dpg.draw_rectangle(pmin=[150, 5], pmax=[345, 65], color=[0, 255, 255, 255], thickness=5)
            # pmin = esquina superior izquierda, pmax = esquina inferior derecha
        dpg.add_text("Prueba DearPyGUI", pos = [200, 50], color = [0, 255, 255, 255])  

        # CREAR BOTONES
        button1 = dpg.add_button(label="Presiona para ver mensaje", pos = [163, 110], callback = press_button1)
        # callback es la función que ejecutará al pulsarlo. Si no lo ponemos, no hace nada
        # Si no pasamos datos, la función que pongamos tiene que estar sin paréntesis

        button2 = dpg.add_button(label="Presiona para insertar datos", pos = [155, 145], callback = press_button2) 

def press_button1(sender, data):  # Estos 2 parámetros hay que ponerlos siempre
    with dpg.window(label="Botón pulsado", width=200, height=100, pos = [150, 220], tag="ventana_secundaria"):
        # tag es un identificador único de cada item (label puede repetirse)
        # Lo usamos para referirnos a este objeto dentro del programa de forma interna: p.ej: para eliminar la ventana
        dpg.add_text("¡Has presionado el botón!", color = [0, 255, 255, 255])  
        button3 = dpg.add_button(label="Cerrar", pos = [75, 50], callback = lambda s, d: close_window(s, d, "ventana_secundaria"))
        # Como tenemos que pasarle parámetros, hay que poner paréntesis. Usamos lambda.
        # lambda: hace que no se llame a la función directamente, solo al pulsar el botón

def close_window(sender, data, tag):
    dpg.delete_item(tag)

def show_data(sender, data, tag): 
    name = dpg.get_value("input_nombre")
    age = dpg.get_value("input_edad")
    close_window(sender, data, tag)  # Cierra la ventana para que la otra salga encima
    
    # Muestra datos insertados en una ventana nueva
    with dpg.window(label="Datos insertados", width=200, height=100, pos = [150, 220], tag="ventana_mostrar_datos"):
        dpg.add_text(f"Nombre: {name}")  
        dpg.add_text(f"Edad: {age}")  
        # Boton para cerrar
        dpg.add_button(label="OK", callback = lambda s, d: close_window(s, d, "ventana_mostrar_datos"))
    
def press_button2(sender, data):
    with dpg.window(label="Insertar datos", width=220, height=180, pos = [150, 220], tag="ventana_insertar_datos"):

        dpg.add_text("Ingrese su nombre:")
        dpg.add_input_text(tag="input_nombre")  # Campo de entrada para el nombre
    
        dpg.add_text("Ingrese su edad:")
        dpg.add_input_text(tag="input_edad")  # Campo de entrada para la edad
        
        # Botón para enviar los datos
        # Sale una ventana donde se muestran los datos
        dpg.add_button(label="Enviar", callback= lambda s, d: show_data(s, d, "ventana_insertar_datos"))

        # Botón para cerrar
        dpg.add_button(label="Cerrar", callback = lambda s, d: close_window(s, d, "ventana_insertar_datos"))
        
def main():
    dpg.create_context() # Antes de llamar a ninguna ventana, es lo primero que hay que hacer

    ventana() # Crear la ventana principal

    # Iniciar la ventana. Si no lo ponemos, la ventana no se muestra
    dpg.setup_dearpygui()
    dpg.show_viewport()
    # Activa el ciclo de eventos para que la aplicación responda a lo que hagamos

    dpg.start_dearpygui()  # Controlar el ciclo de Dear PyGui.

    dpg.destroy_context()  # Limpiar el contexto cuando se cierre. Ponerlo siempre

if __name__ == "__main__":
    main()