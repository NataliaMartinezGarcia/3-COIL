import tkinter as tk 
# from tkinter import messagebox, filedialog, ttk  
# import pandas as pd 
# import sqlite3 
from gui import ScrollApp

def main():
    ventana = tk.Tk()  # Ventana principal
    app = ScrollApp(ventana)
    ventana.mainloop()  # Inicia el bucle principal de la aplicación

if __name__ == "__main__":
    main()