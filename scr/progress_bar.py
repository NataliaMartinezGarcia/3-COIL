import tkinter as tk
from tkinter import ttk
import threading
from typing import Any, Callable, Optional

class LoadingIndicator:
    """A popup window showing an indeterminate progress bar."""
    
    WINDOW_SIZE = "300x100"
    
    STYLES = {
        'BACKGROUND': '#d0d7f2',
        'TEXT_COLOR': '#6677B8',
        'FONT': ("DejaVu Sans Mono", 11),
        'PROGRESS_LENGTH': 200,
        'PROGRESS_SPEED': 15,
        'PADDING': 10,
        'TEXT_PADDING': 5
    }
    
    def __init__(self, parent: tk.Tk):
        """Initialize loading indicator.
        
        Args:
            parent: Parent window for the loading popup
        """
        self.parent = parent
        self.popup: Optional[tk.Toplevel] = None
        self.progress: Optional[ttk.Progressbar] = None
        self.label: Optional[tk.Label] = None
    
    def start(self, message: str = "Loading...") -> None:
        """Display loading indicator popup.
        
        Args:
            message: Text to display below progress bar
        """
        self._create_popup_window()
        self._center_popup()
        self._create_progress_bar()
        self._create_message_label(message)
        self._start_animation()
    
    def _create_popup_window(self) -> None:
        """Create and configure the popup window."""
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("Loading")
        self.popup.geometry(self.WINDOW_SIZE)
        self.popup.resizable(False, False)
        self.popup.transient(self.parent)
        self.popup.grab_set()
        self.popup.config(bg=self.STYLES['BACKGROUND'])
    
    def _center_popup(self) -> None:
        """Center popup window relative to parent."""
        self.popup.update_idletasks()
        
        # Calculate center position
        x = (
            self.parent.winfo_x() +
            (self.parent.winfo_width() - self.popup.winfo_width()) // 2
        )
        y = (
            self.parent.winfo_y() +
            (self.parent.winfo_height() - self.popup.winfo_height()) // 2
        )
        
        self.popup.geometry(f"+{x}+{y}")
    
    def _create_progress_bar(self) -> None:
        """Create and configure the progress bar."""
        self.progress = ttk.Progressbar(
            self.popup,
            mode='indeterminate',
            length=self.STYLES['PROGRESS_LENGTH']
        )
        self.progress.pack(pady=self.STYLES['PADDING'])
    
    def _create_message_label(self, message: str) -> None:
        """Create label with loading message.
        
        Args:
            message: Text to display
        """
        self.label = tk.Label(
            self.popup,
            text=message,
            bg=self.STYLES['BACKGROUND'],
            fg=self.STYLES['TEXT_COLOR'],
            font=self.STYLES['FONT']
        )
        self.label.pack(pady=self.STYLES['TEXT_PADDING'])
    
    def _start_animation(self) -> None:
        """Start progress bar animation and update display."""
        if self.progress:
            self.progress.start(self.STYLES['PROGRESS_SPEED'])
        if self.popup:
            self.popup.update()
    
    def stop(self) -> None:
        """Stop and destroy the loading indicator."""
        if self.progress:
            self.progress.stop()
            
        if self.popup:
            self.popup.grab_release()
            self.popup.destroy()
            self.popup = None
            self.progress = None
            self.label = None

def run_with_loading(
    parent: tk.Tk,
    func: Callable,
    message: str = "Loading...",
    *args: Any,
    **kwargs: Any
) -> Any:
    """Execute a function while displaying a loading indicator.
    
    Args:
        parent: Parent window
        func: Function to execute
        message: Loading message to display
        *args: Positional arguments for func
        **kwargs: Keyword arguments for func
        
    Returns:
        Result from func execution
        
    Raises:
        Exception: Any exception raised by func
    """
    loading = LoadingIndicator(parent)
    result = None
    error = None
    
    def worker() -> None:
        """Execute function in separate thread."""
        nonlocal result, error
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            error = e
    
    # Start loading animation
    loading.start(message)
    
    # Run function in background
    thread = threading.Thread(target=worker)
    thread.start()
    
    # Update GUI while waiting
    while thread.is_alive():
        parent.update()
    
    # Clean up
    loading.stop()
    
    # Handle errors
    if error:
        raise error
    
    return result