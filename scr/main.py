import tkinter as tk
from gui import ScrollApp

def main():
    ventana = tk.Tk()  # Main window
    app = ScrollApp(ventana)
    ventana.mainloop()  # Starts the window loop for the app to run


if __name__ == "__main__":
    main()
