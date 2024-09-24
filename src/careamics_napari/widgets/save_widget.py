 
from typing import Optional
from typing_extensions import Self

from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QPushButton,
    QComboBox
)

from careamics_napari.widgets import (
    PowerOfTwoSpinBox, 
    create_progressbar, 
    PredictDataWidget
)
from careamics_napari.signals import (
    TrainingStatus, 
    TrainingState
)

class SaveWidget(QGroupBox):

    def __init__(
            self: Self,
            train_status: Optional[TrainingStatus] = None
    ) -> None:
        super().__init__()

        self.train_status = train_status

        self.setTitle("Save")
        self.setLayout(QVBoxLayout())

        # Save button
        save_widget = QWidget()
        save_widget.setLayout(QHBoxLayout())
        self.save_choice = QComboBox()
        self.save_choice.addItems(["Bioimage.io", "Checkpoint"]) # TODO move defaults elsewhere
        self.save_choice.setToolTip('Output format')

        self.save_button = QPushButton("Save model", self)
        self.save_button.setEnabled(False)
        self.save_choice.setToolTip('Save the model weights and configuration.')

        save_widget.layout().addWidget(self.save_button)
        save_widget.layout().addWidget(self.save_choice)
        self.layout().addWidget(save_widget)

        # actions
        if self.train_status is not None:
            self.train_status.events.state.connect(self._update_training_state)
            self.save_button.clicked.connect(self._save_model)

    def _update_training_state(self, state: TrainingState):
        if state == TrainingState.DONE or state == TrainingState.STOPPED:
            self.save_button.setEnabled(True)
        elif state == TrainingState.IDLE:
            self.save_button.setEnabled(False)

    def _save_model(self):
        pass # TODO: another signal with states and config?
