

from typing import Optional
from typing_extensions import Self

from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QPushButton,
)

from careamics_napari.signals import TrainingStatus, TrainingState

class TrainingWidget(QGroupBox):
        
    def __init__(
            self: Self,
            signal: Optional[TrainingStatus] = None
    ) -> None:
        super().__init__() # TODO needed? and in the other classes? to pass parent?

        self.train_status = signal

        self.setTitle("Train")
        self.setLayout(QVBoxLayout())

        # train buttons
        train_buttons = QWidget()
        train_buttons.setLayout(QHBoxLayout())

        self.train_button = QPushButton('Train', self)

        self.reset_model_button = QPushButton('', self)
        self.reset_model_button.setEnabled(False)
        self.reset_model_button.setToolTip(
            'Reset the weights of the model (forget the training)'
        )

        train_buttons.layout().addWidget(self.reset_model_button)
        train_buttons.layout().addWidget(self.train_button)
        self.layout().addWidget(train_buttons)

        # actions
        if self.train_status is not None:
            # what to do when the buttons are clicked
            self.train_button.clicked.connect(self._train_stop_clicked)
            self.reset_model_button.clicked.connect(self._reset_clicked)

            # listening to the signal
            self.train_status.events.state.connect(self._update_button)

    def _train_stop_clicked(self):
        if self.train_status is not None:
            if (
                self.train_status.state == TrainingState.IDLE
                or self.train_status.state == TrainingState.DONE
            ):
                self.train_status.state = TrainingState.TRAINING
                self.reset_model_button.setEnabled(False)
                self.reset_model_button.setText("")
                self.train_button.setText('Stop')

            elif self.train_status.state == TrainingState.TRAINING:
                self.train_status.state = TrainingState.STOPPED
                self.train_button.setText('Train')
                self.reset_model_button.setEnabled(True)
                self.reset_model_button.setText("Reset")

            elif self.train_status.state == TrainingState.STOPPED:
                self.train_status.state = TrainingState.TRAINING
                self.train_button.setText('Stop')


    def _reset_clicked(self):
        if self.train_status is not None:
            if self.train_status.state != TrainingState.TRAINING:
                self.train_status.state = TrainingState.IDLE
                self.train_button.setText('Train')
                self.reset_model_button.setEnabled(False)
                self.reset_model_button.setText("")


    def _update_button(self, new_state: TrainingState):
        if (
            new_state == TrainingState.DONE 
            or new_state == TrainingState.STOPPED
        ):
            self.train_button.setText('Train')
            self.reset_model_button.setEnabled(True)
            self.reset_model_button.setText("Reset")
        elif new_state == TrainingState.CRASHED:
            self._reset_clicked()


if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # create signal
    signal = TrainingStatus()

    # Instantiate widget
    widget = TrainingWidget(signal)

    # Show the widget
    widget.show()

    # Run the application event loop
    sys.exit(app.exec_())