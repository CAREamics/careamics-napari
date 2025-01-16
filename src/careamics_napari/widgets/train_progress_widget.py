"""A widget displaying the training progress using two progress bars."""

from typing import Optional

from qtpy.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
)
from typing_extensions import Self

from careamics_napari.signals import TrainingSignal, TrainingState, TrainingStatus
from careamics_napari.widgets import TBPlotWidget, create_progressbar


class TrainProgressWidget(QGroupBox):
    """A widget displaying the training progress using two progress bars.

    Parameters
    ----------
    train_status : TrainingStatus or None, default=None
        Signal representing the training status.
    train_config : TrainingSignal or None, default=None
        Signal representing the training parameters.
    """

    def __init__(
        self: Self,
        train_status: Optional[TrainingStatus] = None,
        train_config: Optional[TrainingSignal] = None,
    ) -> None:
        """Initialize the widget.

        Parameters
        ----------
        train_status : TrainingStatus or None, default=None
            Signal representing the training status.
        train_config : TrainingSignal or None, default=None
            Signal representing the training parameters.
        """
        super().__init__()

        self.train_status = (
            train_status
            if train_status is not None  # for typing purposes
            else TrainingStatus()  # type: ignore
        )

        self.setTitle("Training progress")
        self.setLayout(QVBoxLayout())

        # progress bars
        self.layout().setContentsMargins(20, 20, 20, 0)

        self.pb_epochs = create_progressbar(
            max_value=self.train_status.max_epochs,
            text_format=f"Epoch ?/{self.train_status.max_epochs}",
            value=0,
        )

        self.pb_batch = create_progressbar(
            max_value=self.train_status.max_batches,
            text_format=f"Batch ?/{self.train_status.max_batches}",
            value=0,
        )

        self.layout().addWidget(self.pb_epochs)
        self.layout().addWidget(self.pb_batch)

        # plot widget
        self.plot = TBPlotWidget(
            max_width=300, max_height=300, min_height=250, train_signal=train_config
        )
        self.layout().addWidget(self.plot.native)

        # actions
        if self.train_status is not None:
            self.train_status.events.state.connect(self._update_training_state)

            self.train_status.events.epoch_idx.connect(self._update_epoch)
            self.train_status.events.max_epochs.connect(self._update_max_epoch)
            self.train_status.events.batch_idx.connect(self._update_batch)
            self.train_status.events.max_batches.connect(self._update_max_batch)
            self.train_status.events.val_loss.connect(self._update_loss)

    def _update_training_state(self: Self, state: TrainingState) -> None:
        """Update the widget according to the training state.

        Parameters
        ----------
        state : TrainingState
            Training state.
        """
        if state == TrainingState.IDLE or state == TrainingState.TRAINING:
            self.plot.clear_plot()

    def _update_max_epoch(self: Self, max_epoch: int):
        """Update the maximum number of epochs in the progress bar.

        Parameters
        ----------
        max_epoch : int
            Maximum number of epochs.
        """
        self.pb_epochs.setMaximum(max_epoch)

    def _update_epoch(self: Self, epoch: int) -> None:
        """Update the epoch progress bar.

        Parameters
        ----------
        epoch : int
            Current epoch.
        """
        self.pb_epochs.setValue(epoch + 1)
        self.pb_epochs.setFormat(f"Epoch {epoch+1}/{self.train_status.max_epochs}")

    def _update_max_batch(self: Self, max_batches: int) -> None:
        """Update the maximum number of batches in the progress bar.

        Parameters
        ----------
        max_batches : int
            Maximum number of batches.
        """
        self.pb_batch.setMaximum(max_batches)

    def _update_batch(self: Self) -> None:
        """Update the batch progress bar."""
        self.pb_batch.setValue(self.train_status.batch_idx + 1)
        self.pb_batch.setFormat(
            f"Batch {self.train_status.batch_idx+1}/{self.train_status.max_batches}"
        )

    def _update_loss(self: Self) -> None:
        """Update the loss plot."""
        self.plot.update_plot(
            epoch=self.train_status.epoch_idx,
            train_loss=self.train_status.loss,
            val_loss=self.train_status.val_loss,
        )


if __name__ == "__main__":
    import sys

    from qtpy.QtWidgets import QApplication

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # create signal
    signal = TrainingStatus()  # type: ignore

    # Instantiate widget
    widget = TrainProgressWidget(signal)

    # Show the widget
    widget.show()

    # Run the application event loop
    sys.exit(app.exec_())
