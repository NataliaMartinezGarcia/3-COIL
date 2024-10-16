from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget 
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty



def VentanaAviso():
    texto = Label(text = 'Presionaste el botón !')
    ventana = Popup(title = 'Aviso',content = texto, size_hint = (None,None),size = (400,400))
    ventana.open()

def VentanaDatos(nombre,edad):
    texto = Label(text = f'Tu nombre es {nombre} y tu edad {edad}')
    ventana = Popup(title = 'Aviso',content = texto , size_hint = (None,None),size = (400,400))
    ventana.open()
    


class Manager(ScreenManager):
    pass

class Menu(Screen):
    def AbrirVentana(self):
        VentanaAviso()

class PantallaDatos(Screen):
    nombre = ObjectProperty(None)
    edad = ObjectProperty(None)
    def AbrirVentana(self):
        VentanaDatos(self.nombre.text,self.edad.text)

# Carga la estética del archivo seleccionado
interfaz = Builder.load_file('interfaz.kv')


#La clase que hace la aplicación en si
class Aplicacion(App): 
    def build(self):
        return interfaz  # Devuelve la estética



if __name__ == '__main__':
    Aplicacion().run()
