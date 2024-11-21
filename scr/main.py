import tkinter as tk
from gui import ScrollApp

def main():
    ventana = tk.Tk()  # Ventana principal
    app = ScrollApp(ventana)
    ventana.mainloop()  # Inicia el bucle principal de la aplicación


if __name__ == "__main__":
    main()
