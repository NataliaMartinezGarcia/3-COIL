import tkinter as tk

class ColumnMenu:
    """
    A graphical interface for selecting input and output columns from a DataFrame.
    This class provides a GUI that allows users to select one input column (feature)
    and one output column (target) from a DataFrame using Tkinter widgets. It includes
    scrollable listboxes for both feature and target selection, along with a confirmation
    button to validate the selection.
    """

    def __init__(self, frame: tk.Frame, columns: list, manager):
        """
        Initialize the column selection interface.

        Parameters:
            - frame: Parent frame where widgets will be placed
            - columns: List of available column names
            - manager: Reference to the MenuManager controller
        """

        self._frame = frame
        self._columns = columns
        self._manager = manager
        self._selected_feature = []
        self._selected_target = []

        self._init_ui()

    def _init_ui(self):
        """Initialize all UI components."""
        # Create the UI elements for feature and target selection
        self.create_features_selector()
        self.create_target_selector()
        self.create_confirm_button()

    @property
    def selected_features(self) -> list:
        """
        Get the list of selected feature column
.
        Returns:
            - list: Names of selected feature column
        """
        return self._selected_feature

    @property
    def selected_target(self) -> list:
        """
        Get the list of selected target column.

        Returns:
            - list: Names of selected taget column
        """
        return self._selected_target

    def _add_scrollbar_to_listbox(self, listbox: tk.Listbox, container: tk.Frame):
        """
        Add a scrollbar to a listbox and configure their interaction.

        Parameters:
            - listbox: Listbox widget to add scrollbar to
            - container: Frame containing the listbox
        """
        # Create scrollbar and link it with listbox
        scrollbar = tk.Scrollbar(
            container,
            orient="vertical",
            command=listbox.yview
        )
        scrollbar.pack(side="right", fill="y")
        # Configure listbox to use scrollbar
        listbox.config(yscrollcommand=scrollbar.set)

    def create_features_selector(self):
        """
        Create the feature columns selector.
        Creates a frame containing a label, a single-selection listbox, and a scrollbar
        for selecting input features. The listbox is bound to the manager's selection
        handler.
        """

        # Create frame for feature selection on the left side
        features_frame = self._create_selector_frame(
            relx=0.03,
            title="Select an input column (feature):"
        )

        # Create listbox container and components
        container = self._create_listbox_container(features_frame)
        self._feature_listbox = self._create_listbox(container)
        self._populate_listbox(self._feature_listbox)
        self._add_scrollbar_to_listbox(self._feature_listbox, container)

    def create_target_selector(self):
        """
        Create the target column selector.

        Creates a frame containing a label, a single-selection listbox, and a scrollbar
        for selecting the target variable. The listbox is bound to the manager's
        selection handler.
        """

        # Create frame for target selection on the right side
        target_frame = self._create_selector_frame(
            relx=0.97,
            title="Select an output column (target):"
        )

        container = self._create_listbox_container(target_frame)
        self._target_listbox = self._create_listbox(container)
        self._populate_listbox(self._target_listbox)
        self._add_scrollbar_to_listbox(self._target_listbox, container)

    def _create_selector_frame(self, relx: float, title: str) -> tk.Frame:
        """
        Create a frame with title for column selection.

        Parameters:
            - relx: Relative x position (0-1) for frame placement
            - title: Text to display as frame title

        Returns:
            - tk.Frame: Configured frame for selection components
        """
        # Create main frame with fixed dimensions
        frame = tk.Frame(
            self._frame,
            width=290,
            height=170,
            bg='#d0d7f2'
        )
        # Position frame using relative coordinates
        frame.place(relx=relx, rely=0.25, relwidth=0.5,
                    anchor="w" if relx < 0.5 else "e")
        # Create and position title label
        label = tk.Label(
            frame,
            text=title,
            fg='#4d598a',
            bg='#d0d7f2',
            font=("DejaVu Sans Mono", 10, 'bold'),
            width=35
        )
        label.place(relx=0.5, rely=0.1, anchor="center")

        return frame

    def _create_listbox_container(self, parent: tk.Frame) -> tk.Frame:
        """
        Create container frame for listbox and scrollbar.

        Parameters:
            - parent: Parent frame to contain the listbox

        Returns:
            - tk.Frame: Container frame for listbox components
        """
        # Create and position container frame
        container = tk.Frame(parent)
        container.place(
            relx=0.5,
            rely=0.5,
            relwidth=0.75,
            relheight=0.5,
            anchor="center"
        )
        return container

    def _create_listbox(self, container: tk.Frame) -> tk.Listbox:
        """
        Create and configure a listbox for column selection.

        Parameters:
            - container: Parent frame for the listbox

        Returns:
            - tk.Listbox: Configured listbox widget
        """
        # Create listbox with single selection mode
        listbox = tk.Listbox(
            container,
            selectmode=tk.SINGLE,
            height=5,
            exportselection=False
        )
        listbox.pack(side="left", fill="both", expand=True)
        # Bind selection event to manager's handler
        listbox.bind("<<ListboxSelect>>", self._manager.on_listbox_select)
        return listbox

    def _populate_listbox(self, listbox: tk.Listbox):
        """
        Fill listbox with column names.

        Parameters:
            - listbox: Listbox widget to populate
        """
        # Add each column name to the listbox
        for column in self._columns:
            listbox.insert(tk.END, column)

    def create_confirm_button(self):
        """
        Create the confirmation button.
        Creates a button that triggers the manager's confirm_selection method when clicked.
        The button is styled with custom colors and fonts.
        """
        # Create styled confirmation button
        confirm_button = tk.Button(
            self._frame,
            text="Confirm selection",
            command=self._manager.confirm_selection,
            font=("Arial", 11, 'bold'),
            fg="#FAF8F9",
            bg='#6677B8',
            activebackground="#808ec6",
            activeforeground="#FAF8F9",
            cursor="hand2"
        )
        # Center button in frame
        confirm_button.place(relx=0.5, rely=0.45, anchor='center')

    def get_selected_columns(self):
        """
        Store the currently selected columns from both listboxes.

        Updates the internal _selected_features and _selected_target lists with
        the current selections from the respective listboxes.

        Returns:
            - None: Updates internal selected columns lists
        """
        # Get selected features from listbox
        self._selected_feature = [
            self._feature_listbox.get(i)
            for i in self._feature_listbox.curselection()
        ]
        # Get selected target from listbox
        self._selected_target = [
            self._target_listbox.get(i)
            for i in self._target_listbox.curselection()
        ]