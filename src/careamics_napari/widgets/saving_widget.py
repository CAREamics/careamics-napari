 
from pathlib import Path
from typing import Optional
from typing_extensions import Self

from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QPushButton,
    QComboBox,
    QFileDialog
)

from careamics_napari.signals import (
    TrainingStatus, 
    TrainingState,
    SavingStatus,
    SavingSignal,
    SavingState,
    ExportType
)

class SavingWidget(QGroupBox):

    def __init__(
            self: Self,
            train_status: Optional[TrainingStatus] = None,
            save_status: Optional[SavingStatus] = None,
            save_signal: Optional[SavingSignal] = None
    ) -> None:
        super().__init__()

        self.train_status = train_status
        self.save_status = save_status
        self.save_signal = save_signal

        self.setTitle("Save")
        self.setLayout(QVBoxLayout())

        # Save button
        save_widget = QWidget()
        save_widget.setLayout(QHBoxLayout())
        self.save_choice = QComboBox()
        self.save_choice.addItems(ExportType.list())
        self.save_choice.setToolTip('Output format')

        self.save_button = QPushButton("Save model", self)
        self.save_button.setEnabled(False)
        self.save_choice.setToolTip('Save the model weights and configuration.')

        save_widget.layout().addWidget(self.save_button)
        save_widget.layout().addWidget(self.save_choice)
        self.layout().addWidget(save_widget)

        # actions
        if self.train_status is not None:
            # updates from signals
            self.train_status.events.state.connect(self._update_training_state)
            
            # when clicking the save button
            self.save_button.clicked.connect(self._save_model)

            # when changing the format
            self.save_choice.currentIndexChanged.connect(self._update_export_type)

    def _update_export_type(self, index: int):
        if self.save_signal is not None:
            self.save_signal.export_type = self.save_choice.currentText()

    def _update_training_state(self, state: TrainingState):
        if state == TrainingState.DONE or state == TrainingState.STOPPED:
            self.save_button.setEnabled(True)
        elif state == TrainingState.IDLE:
            self.save_button.setEnabled(False)

    def _save_model(self):
        if self.save_status is not None:
            if (
                self.save_status.state == SavingState.IDLE
                or self.save_status.state == SavingState.DONE
                or self.save_status.state == SavingState.CRASHED
            ):
                #destination = Path(QFileDialog.getSaveFileName(caption='Save model'))
                destination = Path(QFileDialog.getExistingDirectory(caption='Save model'))
                self.save_signal.path_model = destination

                # trigger saving
                self.save_status.state = SavingState.SAVING


if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # create signal
    train_signal = TrainingStatus()
    save_signal = SavingSignal()
    save_status = SavingStatus()
    
    # Instantiate widget
    widget = SavingWidget(
        train_signal,
        save_status,
        save_signal
    )

    # Show the widget
    widget.show()

    # Run the application event loop
    sys.exit(app.exec_())
