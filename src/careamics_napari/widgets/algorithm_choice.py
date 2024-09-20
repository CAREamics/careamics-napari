"""Algorithm selection widget."""

from qtpy.QtWidgets import (
    QComboBox,
    QWidget,
    QHBoxLayout,
    QLabel
)

from careamics_napari.careamics_utils import get_available_algorithms


def create_algorithm_choice() -> QWidget:
    """Create a widget for selecting the algorithm.

    Returns
    -------
    QWidget
        A widget for selecting the algorithm.
    """
    # Create layout
    widget = QWidget()
    layout = QHBoxLayout()

    # Create a label to show the selected item
    label = QLabel("Algorithm")
    layout.addWidget(label)

    # Create a QComboBox (dropdown list)
    combo_box = QComboBox()
    combo_box.addItems(get_available_algorithms())
    combo_box.setToolTip("Select an algorithm.")

    layout.addWidget(combo_box)
    
    # # Connect the signal to handle item selection
    # combo_box.currentIndexChanged.connect(update_label)
    
    widget.setLayout(layout)
    return widget


if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    # Step 2: Create a QApplication instance
    app = QApplication(sys.argv)

    # Step 4: Instantiate your widget
    widget = create_algorithm_choice()

    # Step 5: Show the widget
    widget.show()

    # Step 6: Run the application event loop
    sys.exit(app.exec_())
