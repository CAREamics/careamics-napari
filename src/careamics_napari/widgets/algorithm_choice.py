"""Algorithm selection widget."""

from typing import Optional

from qtpy.QtWidgets import (
    QComboBox,
    QWidget,
    QHBoxLayout,
    QLabel
)

from careamics_napari.careamics_utils import get_available_algorithms, get_algorithm
from careamics_napari.widgets.signals import AlgorithmSignal


class AlgorithmChoiceWidget(QWidget):

    def __init__(self, signal: Optional[AlgorithmSignal] = None):
        super().__init__()

        self.signal = signal

        # Create layout
        layout = QHBoxLayout()

        # Create a label to show the selected item
        label = QLabel("Algorithm")
        layout.addWidget(label)

        # Create a QComboBox (dropdown list)
        self.combo_box = QComboBox()
        self.combo_box.addItems(get_available_algorithms())
        self.combo_box.setToolTip("Select an algorithm.")

        layout.addWidget(self.combo_box)
        
        # Connect the signal
        self.combo_box.currentIndexChanged.connect(self.algorithm_changed)
        self.current_algorithm = self._get_current_algorithm()

        self.setLayout(layout)

    def _get_current_algorithm(self) -> str:
        """Return the current algorithm name.

        Returns
        -------
        str
            Current algorithm name.
        """
        return get_algorithm(self.combo_box.currentText())

    def algorithm_changed(self, index: int) -> None:
        """Emit the algorithm signal.
        
        Parameters
        ----------
        index : int
            Index of the selected algorithm.
        """
        # save SupportedAlgorithm
        self.current_algorithm = self._get_current_algorithm()

        # emit the signal
        if self.signal is not None:
            self.signal.name = self.current_algorithm


if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    myalgo = AlgorithmSignal("")

    @myalgo.events.name.connect
    def print_algorithm(name: str):
        print(f"Selected algorithm: {name}")

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Instantiate widget
    widget = AlgorithmChoiceWidget(myalgo)

    # Show the widget
    widget.show()

    # Run the application event loop
    sys.exit(app.exec_())