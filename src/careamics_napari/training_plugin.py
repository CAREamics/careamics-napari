"""CAREamics training Qt widget."""
from enum import Enum
from typing import Optional, Any
from typing_extensions import Self

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget 
)

from careamics.config.support import SupportedAlgorithm
from careamics_napari.widgets import (
    CAREamicsBanner,
    create_gpu_label,
    AlgorithmChoiceWidget,
    DataSelectionWidget,
    ScrollWidgetWrapper,
    ConfigurationWidget,
    TrainingWidget
)
from careamics_napari.widgets.signals import ConfigurationSignal, TrainingStatus

class State(Enum):
    IDLE = 0
    RUNNING = 1

class TrainingWidgetWrapper(ScrollWidgetWrapper):
    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        super().__init__(TrainPlugin(*args, **kwargs))


class TrainPlugin(QWidget):
    def __init__(
            self: Self,
            configuration_signal: Optional[ConfigurationSignal] = None,
            train_signal: Optional[TrainingStatus] = None
    ) -> None:
        super().__init__()

        # add signal
        self.configuration_signal = configuration_signal
        self.train_signal = train_signal

        self.init_ui()

    def init_ui(self) -> None:
        """Assemble the widgets."""

        # layout
        self.setLayout(QVBoxLayout())
        self.setMinimumWidth(200)

        # add banner
        self.layout().addWidget(
            CAREamicsBanner(
                title_label="CAREamics",
                short_desc=(
                    "CAREamics UI for training denoising model."
                )
            )
        )

        # add GPU label and algorithm selection
        algo_panel = QWidget()
        algo_panel.setLayout(QHBoxLayout())
        
        gpu_button = create_gpu_label()
        gpu_button.setAlignment(Qt.AlignmentFlag.AlignRight)
        gpu_button.setContentsMargins(0, 5, 0, 0) # top margin

        algo_choice = AlgorithmChoiceWidget(signal=self.configuration_signal)
        gpu_button.setAlignment(Qt.AlignmentFlag.AlignLeft)

        algo_panel.layout().addWidget(algo_choice)
        algo_panel.layout().addWidget(gpu_button)

        self.layout().addWidget(algo_panel)

        # add data tabs
        self.data_stck = QStackedWidget()
        self.data_layers = [
            DataSelectionWidget(self.configuration_signal),
            DataSelectionWidget(self.configuration_signal, True),
        ]
        for layer in self.data_layers:
            self.data_stck.addWidget(layer)
        self.data_stck.setCurrentIndex(0)

        self.layout().addWidget(self.data_stck)

        # add configuration widget
        self.config_widget = ConfigurationWidget(self.configuration_signal)
        self.layout().addWidget(self.config_widget)

        # add train widget
        self.train_widget = TrainingWidget(self.train_signal)
        self.layout().addWidget(self.train_widget)


        # connect signals
        if self.configuration_signal is not None:
            self.configuration_signal.events.algorithm.connect(self._set_data_from_algorithm)
            self._set_data_from_algorithm(self.configuration_signal.algorithm)
            
    def _set_data_from_algorithm(self, name: str) -> None:
        """Set the data selection widget based on the algorithm."""
        print(name)
        if (
            name == SupportedAlgorithm.CARE.value
            or name == SupportedAlgorithm.N2N.value
        ):
            self.data_stck.setCurrentIndex(1)
        else:
            self.data_stck.setCurrentIndex(0)



if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Signals
    myalgo = ConfigurationSignal()
    mytrain = TrainingStatus()

    # Instantiate widget
    widget = TrainingWidgetWrapper(myalgo, mytrain)

    # Show the widget
    widget.show()

    # Run the application event loop
    sys.exit(app.exec_())