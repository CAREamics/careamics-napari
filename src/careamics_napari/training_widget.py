"""CAREamics training Qt widget."""
from enum import Enum
from typing_extensions import Self

from qtpy import QtGui
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QGroupBox,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFormLayout,
    QComboBox,
    QFileDialog,
    QLabel,
    QTabWidget,
    QCheckBox
)

from careamics_napari.widgets import (
    CAREamicsBanner,
    create_gpu_label,
    AlgorithmChoiceWidget,
    create_tabs,
    ScrollWidgetWrapper,
)

class State(Enum):
    IDLE = 0
    RUNNING = 1

class TrainingWidgetWrapper(ScrollWidgetWrapper):
    def __init__(self: Self) -> None:
        super().__init__(TrainWidget())


class TrainWidget(QWidget):
    def __init__(self: Self) -> None:
        super().__init__()

        self.init_ui()

    def init_ui(self) -> None:
        """Assemble the widgets."""

        # layout
        self.setLayout(QVBoxLayout())
        self.setMinimumWidth(200)

        # add banner
        self.layout().addWidget(
            CAREamicsBanner(
                title="CAREamics",
                short_desc="CAREamics UI for training a denoising model.",
            )
        )

        # add GPU label
        gpu_button = create_gpu_label()
        gpu_button.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout().addWidget(gpu_button)

        # add algorithm selection
        self.layout().addWidget(AlgorithmChoiceWidget())

        # add data tabs
        self.layout().addWidget(create_tabs())



if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Instantiate widget
    widget = TrainingWidgetWrapper()

    # Show the widget
    widget.show()

    # Run the application event loop
    sys.exit(app.exec_())