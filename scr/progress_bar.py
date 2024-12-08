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

        Parameters:
            - parent: Parent window for the loading popup
        """
        self._parent = parent
        self._popup: Optional[tk.Toplevel] = None
        self._progress: Optional[ttk.Progressbar] = None
        self._label: Optional[tk.Label] = None

    def start(self, message: str = "Loading...") -> None:
        """Display loading indicator popup.

        Parameters:
            - message: Text to display below progress bar
        """
        self._create_popup_window()
        self._center_popup()
        self._create_progress_bar()
        self._create_message_label(message)
        self._start_animation()

    def _create_popup_window(self) -> None:
        """Create and configure the popup window."""
        self._popup = tk.Toplevel(self._parent)
        self._popup.title("Loading")
        self._popup.geometry(self.WINDOW_SIZE)
        self._popup.resizable(False, False)
        self._popup.transient(self._parent)
        self._popup.grab_set()
        self._popup.config(bg=self.STYLES['BACKGROUND'])

    def _center_popup(self) -> None:
        """Center popup window relative to parent."""
        self._popup.update_idletasks()

        # Calculate center position
        x = (
            self._parent.winfo_x() +
            (self._parent.winfo_width() - self._popup.winfo_width()) // 2
        )
        y = (
            self._parent.winfo_y() +
            (self._parent.winfo_height() - self._popup.winfo_height()) // 2
        )

        self._popup.geometry(f"+{x}+{y}")

    def _create_progress_bar(self) -> None:
        """Create and configure the progress bar."""
        self._progress = ttk.Progressbar(
            self._popup,
            mode='indeterminate',
            length=self.STYLES['PROGRESS_LENGTH']
        )
        self._progress.pack(pady=self.STYLES['PADDING'])

    def _create_message_label(self, message: str) -> None:
        """Create label with loading message.

        Parameters:
            - message: Text to display
        """
        self._label = tk.Label(
            self._popup,
            text=message,
            bg=self.STYLES['BACKGROUND'],
            fg=self.STYLES['TEXT_COLOR'],
            font=self.STYLES['FONT']
        )
        self._label.pack(pady=self.STYLES['TEXT_PADDING'])

    def _start_animation(self) -> None:
        """Start progress bar animation and update display."""
        if self._progress:
            self._progress.start(self.STYLES['PROGRESS_SPEED'])
        if self._popup:
            self._popup.update()

    def stop(self) -> None:
        """Stop and destroy the loading indicator."""
        if self._progress:
            self._progress.stop()

        if self._popup:
            self._popup.grab_release()
            self._popup.destroy()
            self._popup = None
            self._progress = None
            self._label = None


def run_with_loading(
    parent: tk.Tk,
    func: Callable,
    message: str = "Loading...",
    *Parameters: Any,
    **kwParameters: Any
) -> Any:
    """Execute a function while displaying a loading indicator.

    Parameters:
        - parent: Parent window
        - func: Function to execute
        - message: Loading message to display
        - *Parameters: Positional arguments for func
        - **kwParameters: Keyword arguments for func

    Returns:
        - Result from func execution

    Raises:
        - Exception: Any exception raised by func
    """
    loading = LoadingIndicator(parent)
    result = None
    error = None

    def worker() -> None:
        """Execute function in separate thread."""
        nonlocal result, error
        try:
            result = func(*Parameters, **kwParameters)
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
