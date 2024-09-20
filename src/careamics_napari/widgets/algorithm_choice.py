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


class AlgorithmChoiceWidget(QComboBox):

    def __init__(self, signal: Optional[AlgorithmSignal] = None):
        super().__init__()

        self.signal = signal

        self.addItems(get_available_algorithms())
        self.setToolTip("Select an algorithm.")
        
        # Connect the signal
        self.currentIndexChanged.connect(self.algorithm_changed)
        self.current_algorithm = self._get_current_algorithm()

    def _get_current_algorithm(self) -> str:
        """Return the current algorithm name.

        Returns
        -------
        str
            Current algorithm name.
        """
        return get_algorithm(self.currentText())

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

    myalgo = AlgorithmSignal()

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