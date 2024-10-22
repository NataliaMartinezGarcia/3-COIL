import tkinter as tk 
# from tkinter import messagebox, filedialog, ttk  
# import pandas as pd 
# import sqlite3 
from gui import DataExplorerApp

def main():
    ventana = tk.Tk()  # Ventana principal
    app = DataExplorerApp(ventana)
    ventana.mainloop()  # Inicia el bucle principal de la aplicación

if __name__ == "__main__":
    main()