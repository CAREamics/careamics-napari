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

from careamics.config.support import SupportedAlgorithm
from careamics_napari.widgets import (
    CAREamicsBanner,
    create_gpu_label,
    AlgorithmChoiceWidget,
    TrainDataWidget,
    ScrollWidgetWrapper,
    ConfigurationWidget,
    TrainingWidget,
    TrainProgressWidget,
    PredictionWidget
)
from careamics_napari.signals import (
    TrainConfigurationSignal, 
    TrainingStatus, 
    TrainingState,
    TrainUpdate,
    TrainUpdateType,
    PredConfigurationSignal,
    PredictionState,
    PredictionStatus,
    PredictionUpdate,
    PredictionUpdateType
)
from careamics_napari.careamics_utils import train_worker, free_memory

if TYPE_CHECKING:
    import napari

# at run time
try:
    import napari
except ImportError:
    _has_napari = False
else:
    _has_napari = True

# TODO: add logging to napari

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
        self.train_config_signal = TrainConfigurationSignal()
        self.train_signal = TrainingStatus()
        self.pred_config_signal = PredConfigurationSignal()
        self.pred_signal = PredictionStatus()

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

        algo_choice = AlgorithmChoiceWidget(signal=self.train_config_signal)
        gpu_button.setAlignment(Qt.AlignmentFlag.AlignLeft)

        algo_panel.layout().addWidget(algo_choice)
        algo_panel.layout().addWidget(gpu_button)

        self.layout().addWidget(algo_panel)

        # add data tabs
        self.data_stck = QStackedWidget()
        self.data_layers = [
            TrainDataWidget(signal=self.train_config_signal),
            TrainDataWidget(
                signal=self.train_config_signal, use_target=True
            ),
        ]
        for layer in self.data_layers:
            self.data_stck.addWidget(layer)
        self.data_stck.setCurrentIndex(0)

        self.layout().addWidget(self.data_stck)

        # add configuration widget
        self.config_widget = ConfigurationWidget(self.train_config_signal)
        self.layout().addWidget(self.config_widget)

        # add train widget
        self.train_widget = TrainingWidget(self.train_signal)
        self.layout().addWidget(self.train_widget)

        # add progress widget
        self.progress_widget = TrainProgressWidget(self.train_signal)
        self.layout().addWidget(self.progress_widget)

        # add prediction
        self.prediction_widget = PredictionWidget(
            self.train_signal,
            self.pred_signal,
            self.train_config_signal,
            self.pred_config_signal
        )

        # add saving
        # TODO

        # connect signals
        if self.train_config_signal is not None:
            # changes from the selected algorithm
            self.train_config_signal.events.algorithm.connect(self._set_data_from_algorithm)
            self._set_data_from_algorithm(self.train_config_signal.algorithm) # force update

            # changes from the training or prediction state
            self.train_signal.events.state.connect(self._training_state_changed)
            self.pred_signal.events.state.connect(self._prediction_state_changed)

    def _training_state_changed(self, state: TrainingState) -> None:
        if state == TrainingState.TRAINING:
            self.train_worker = train_worker(
                self.train_config_signal,
                self.careamist
            )
            
            self.train_worker.yielded.connect(self._update_from_training)
            self.train_worker.start()

        elif state == TrainingState.STOPPED:
            if self.careamist is not None:
                self.careamist.stop_training()

        elif state == TrainingState.CRASHED or state == TrainingState.IDLE:
            if self.careamist is not None:
                del self.careamist
                self.careamist = None

    def _prediction_state_changed(self, state: PredictionState) -> None:
        if state == PredictionState.PREDICTING:
            self.pred_worker = None # TODO
            
            # self.pred_worker.yielded.connect(self._update)
            # self.pred_worker.start()

        elif state == PredictionState.STOPPED:
            # if self.careamist is not None:
            #     self.careamist.stop_prediction()
            # TODO
            pass

    def _update_from_training(self, update: TrainUpdate) -> None:
        """Update the signal from the training worker."""
        if update.type == TrainUpdateType.CAREAMIST:
            self.careamist = update.value
        elif update.type == TrainUpdateType.DEBUG:
            print(update.value)
        elif update.type == TrainUpdateType.EXCEPTION:
            self.train_signal.state = TrainingState.CRASHED
            raise update.value
        else:
            self.train_signal.update(update)
            
    def _set_data_from_algorithm(self, name: str) -> None:
        """Set the data selection widget based on the algorithm."""
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