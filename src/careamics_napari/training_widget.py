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



if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    # Step 2: Create a QApplication instance
    app = QApplication(sys.argv)

    # Step 4: Instantiate your widget
    widget = TrainingWidgetWrapper()

    # Step 5: Show the widget
    widget.show()

    # Step 6: Run the application event loop
    sys.exit(app.exec_())
