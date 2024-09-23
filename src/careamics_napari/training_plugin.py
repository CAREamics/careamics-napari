"""CAREamics training Qt widget."""
from typing import Optional, TYPE_CHECKING
from typing_extensions import Self

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget 
)

from careamics import CAREamist
from careamics.config.support import SupportedAlgorithm
from careamics_napari.widgets import (
    CAREamicsBanner,
    create_gpu_label,
    AlgorithmChoiceWidget,
    DataSelectionWidget,
    ScrollWidgetWrapper,
    ConfigurationWidget,
    TrainingWidget,
    ProgressWidget
)
from careamics_napari.signals import (
    ConfigurationSignal, 
    TrainingStatus, 
    TrainingState,
    Update,
    UpdateType
)
from careamics_napari.careamics_utils.training_worker import train_worker

if TYPE_CHECKING:
    import napari

# at run time
try:
    import napari
except ImportError:
    _has_napari = False
else:
    _has_napari = True


class TrainPluginWrapper(ScrollWidgetWrapper):
    def __init__(self: Self, napari_viewer: Optional[napari.Viewer] = None) -> None:
        super().__init__(TrainPlugin(napari_viewer))


class TrainPlugin(QWidget):
    def __init__(
            self: Self,
            napari_viewer: Optional[napari.Viewer] = None,
    ) -> None:
        super().__init__()
        self.viewer = napari_viewer
        self.careamist = None

        # create signals
        self.config_signal = ConfigurationSignal()
        self.train_signal = TrainingStatus()

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

        algo_choice = AlgorithmChoiceWidget(signal=self.config_signal)
        gpu_button.setAlignment(Qt.AlignmentFlag.AlignLeft)

        algo_panel.layout().addWidget(algo_choice)
        algo_panel.layout().addWidget(gpu_button)

        self.layout().addWidget(algo_panel)

        # add data tabs
        self.data_stck = QStackedWidget()
        self.data_layers = [
            DataSelectionWidget(signal=self.config_signal, napari_viewer=self.viewer),
            DataSelectionWidget(
                signal=self.config_signal, use_target=True, napari_viewer=self.viewer
            ),
        ]
        for layer in self.data_layers:
            self.data_stck.addWidget(layer)
        self.data_stck.setCurrentIndex(0)

        self.layout().addWidget(self.data_stck)

        # add configuration widget
        self.config_widget = ConfigurationWidget(self.config_signal)
        self.layout().addWidget(self.config_widget)

        # add train widget
        self.train_widget = TrainingWidget(self.train_signal)
        self.layout().addWidget(self.train_widget)

        # add progress widget
        self.progress_widget = ProgressWidget(self.train_signal)
        self.layout().addWidget(self.progress_widget)

        # connect signals
        if self.config_signal is not None:
            # changes from the selected algorithm
            self.config_signal.events.algorithm.connect(self._set_data_from_algorithm)
            self._set_data_from_algorithm(self.config_signal.algorithm) # force update

            # changes from the training state
            self.train_signal.events.state.connect(self._training_state_changed)

    def _training_state_changed(self, state: TrainingState) -> None:
        if state == TrainingState.TRAINING:
            self.train_worker = train_worker(
                self.config_signal, 
            )
            
            self.train_worker.yielded.connect(self._update)
            self.train_worker.start()

        # elif state == TrainingState.STOPPED:
        #     if self.careamist is not None:
        #         self.careamist.stop_training()

    def _update(self, update: Update) -> None:
        """Update the signal from the training worker."""
        self.train_signal.update(update)
            
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
    # from qtpy.QtWidgets import QApplication
    # import sys

    # # Create a QApplication instance
    # app = QApplication(sys.argv)

    # # Instantiate widget
    # widget = TrainPluginWrapper()

    # # Show the widget
    # widget.show()

    # # Run the application event loop
    # sys.exit(app.exec_())

    import napari
    # create a Viewer
    viewer = napari.Viewer()

    # add napari-n2v plugin
    viewer.window.add_dock_widget(TrainPluginWrapper(viewer))

    # add image to napari
    # viewer.add_image(data[0][0], name=data[0][1]['name'])

    # start UI
    napari.run()