# documentación -> https://wiki.python.org/moin/PyQt

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

"""
# para crear una ventana vacía 
def ventana_vacia():
    app = QApplication([])
    window = QWidget()
    window.show()
    app.exec_()
"""

#para crear una ventana con elementos 
def ventana ():
    app = QApplication([])  # QApplication crea la aplicación
    ventana = QWidget()
    ventana.setGeometry(100,100,400,300) ## .setGeometry cambia el tamaño y posición de la ventana (x, y, width, height)
    ventana.setWindowTitle("Ejemplo de PyQt") # para añadir el título de la ventana 

    #para añadir etiquetas y botones 

    # Layout para organizar los widgets automáticamente
    dist = QVBoxLayout() # QVBoxLayout coloca los widgets en disposición vertical
        #dist = QHBoxLayout # QHBoxLayout coloca los widgets en disposición horizontal

    etiqueta = QLabel("PRUEBA PyQt") # QLabel crea una etiqueta de texto
    etiqueta.setFont(QFont("Arial",20)) # para cambiar el formato("tipo de letra", tamaño)


    boton1 = QPushButton("Presiona para ver mensaje") # QPushButton crea un botón
    boton1.clicked.connect(mensaje)  # .clicked.connect(mensaje) vincula el botón con la función mensaje()

    boton2 = QPushButton("Presiona para insertar datos")
    boton2.clicked.connect(obtener_datos)

    # .addWidget añade los widgets al layout vertical
    dist.addWidget(etiqueta)
    dist.addWidget(boton1)
    dist.addWidget(boton2)

    ventana.setLayout(dist) # .setLayout asigna el layout a la ventana principal
    ventana.show() # .show muestra la ventana en pantalla
    app.exec_() # app.exec_() inicia el bucle de eventos para que la ventana permanezca abierta

# PARA DAR FUNCIONALIDAD A LOS BOTONES

# función para que aparezca un mensaje en otra ventana al presional el bottón 
def mensaje():
    msg_box = QMessageBox() # QMessageBox es un tipo de ventana emergente para mostrar mensajes
    msg_box.setWindowTitle("Mensaje") 
    msg_box.setText("¡Has presionado el botón!")
    msg_box.exec_() # .exec_() muestra la ventana emergente

# función para obtener los datos en una nueva ventana
def obtener_datos ():
    ventana_formulario = QWidget()
    ventana_formulario.setWindowTitle("Formulario")
    ventana_formulario.setGeometry(150, 150, 300, 200)
    
    layout = QVBoxLayout()
    
    label_nombre = QLabel("Nombre completo:")
    input_nombre = QLineEdit() # QLineEdit es un campo de texto donde el usuario puede escribir
    
    label_edad = QLabel("Edad:")
    input_edad = QLineEdit()  
    
    boton_enviar = QPushButton("Enviar") # Botón para enviar los datos

    # Función interna para manejar el evento de envío
    def enviar_datos():
        nombre = input_nombre.text() 
        edad = input_edad.text()
        ventana_formulario.close()  # cerrar la ventana del formulario después de enviar 
        mostrar_datos(nombre, edad)  # Llama a la función mostrar_datos para mostrar los datos ingresados

    boton_enviar.clicked.connect(enviar_datos) # Vincula el botón con la función interna enviar_datos
    
    # Añadir widgets al layout
    layout.addWidget(label_nombre)
    layout.addWidget(input_nombre)
    layout.addWidget(label_edad)
    layout.addWidget(input_edad)
    layout.addWidget(boton_enviar)
    
    ventana_formulario.setLayout(layout)  # Asigna el layout a la ventana
    ventana_formulario.show() # Muestra la ventana del formulario

def mostrar_datos (nombre,edad): 
    mensaje = f"Datos insertados:\nNombre: {nombre}\nEdad: {edad}" # Formatea los datos como un mensaje
    msg_box = QMessageBox()  # Crea una ventana emergente
    msg_box.setWindowTitle("Datos insertados")
    msg_box.setText(mensaje)
    msg_box.exec_() # Muestra la ventana emergente con los datos


if __name__ == "__main__":
    #ventana_vacia()
    ventana()
