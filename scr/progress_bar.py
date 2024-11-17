import tkinter as tk
from tkinter import ttk
import threading

class LoadingIndicator:
    def __init__(self, parent):
        """
        Initialize the loading indicator popup window.
        
        Args:
            parent: The parent window where the loading indicator will be shown
        """
        self.parent = parent
        self.popup = None
        self.progress = None
        self.label = None

    def start(self, message="Loading..."):
        """
        Show the loading indicator as a popup window with a custom message.
        
        Args:
            message (str): Message to display below the progress bar
        """
        # Create popup window
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("Loading")
        self.popup.geometry("300x100")
        self.popup.resizable(False, False)
        self.popup.transient(self.parent)
        self.popup.grab_set()
        self.popup.config(bg='#d0d7f2')

        # Center popup on screen
        self.popup.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.popup.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.popup.winfo_height() // 2)
        self.popup.geometry(f"+{x}+{y}")

        # Create and configure progress bar
        self.progress = ttk.Progressbar(
            self.popup,
            mode='indeterminate',
            length=200
        )
        self.progress.pack(pady=10)

        # Create label for message
        self.label = tk.Label(
            self.popup,
            text=message,
            bg='#d0d7f2',
            fg='#6677B8',
            font=("DejaVu Sans Mono", 11)
        )
        self.label.pack(pady=5)

        # Start progress bar animation
        self.progress.start(15)

        # Force update
        self.popup.update()

    def stop(self):
        """Stop and hide the loading indicator."""
        if self.progress:
            self.progress.stop()
        if self.popup:
            self.popup.grab_release()
            self.popup.destroy()
            self.popup = None
            self.progress = None
            self.label = None


def run_with_loading(parent, func, message="Loading...", *args, **kwargs):
    """
    Run a function with a loading indicator.
    
    Args:
        parent: Parent window
        func: Function to run
        message: Loading message to display
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function
    
    Returns:
        The result of the function execution
    """
    loading = LoadingIndicator(parent)
    result = None
    error = None

    def worker():
        nonlocal result, error
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            error = e

    # Start loading indicator
    loading.start(message)

    # Run function in separate thread
    thread = threading.Thread(target=worker)
    thread.start()

    # Update the GUI while waiting for the thread
    while thread.is_alive():
        parent.update()

    # Stop loading indicator
    loading.stop()

    # If there was an error, raise it
    if error:
        raise error

    return result
