

from typing import Optional
from typing_extensions import Self

from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QPushButton,
    QCheckBox,
    QFormLayout,
    QLabel
)

from careamics_napari.widgets import (
    PowerOfTwoSpinBox, 
    create_progressbar, 
    PredictDataWidget
)
from careamics_napari.signals import (
    TrainingStatus, 
    TrainingState,
    TrainingSignal,
    PredictionStatus, 
    PredictionState,
    PredictionSignal
)

class PredictionWidget(QGroupBox):

    def __init__(
            self: Self,
            train_status: Optional[TrainingStatus] = None,
            pred_status: Optional[PredictionStatus] = None,
            train_config_signal: Optional[TrainingSignal] = None,
            pred_config_signal: Optional[PredictionSignal] = None

    ) -> None:
        super().__init__()

        self.train_status = train_status
        self.pred_status = pred_status
        self.train_config_signal = train_config_signal
        self.pred_config_signal = pred_config_signal
        
        self.setTitle("Prediction")
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(20, 20, 20, 0)

        # data selection
        predict_data_widget = PredictDataWidget(self.pred_config_signal)
        self.layout().addWidget(predict_data_widget)

        # checkbox
        self.tiling_cbox = QCheckBox('Tile prediction')
        self.tiling_cbox.setToolTip(
            'Select to predict the image by tiles, allowing '
            'to predict on large images.'
        )
        self.layout().addWidget(self.tiling_cbox)

        # tiling spinboxes
        self.tile_size_xy = PowerOfTwoSpinBox(
            64, 1024, self.pred_config_signal.tile_size_xy
        )
        self.tile_size_xy.setToolTip('Tile size in the xy dimension.')
        self.tile_size_xy.setEnabled(False)

        self.tile_size_z = PowerOfTwoSpinBox(4, 32, self.pred_config_signal.tile_size_z)
        self.tile_size_z.setToolTip('Tile size in the z dimension.')
        self.tile_size_z.setEnabled(False)

        tiling_form = QFormLayout()
        tiling_form.addRow('XY tile size', self.tile_size_xy)
        tiling_form.addRow('Z tile size', self.tile_size_z)
        tiling_widget = QWidget()
        tiling_widget.setLayout(tiling_form)
        self.layout().addWidget(tiling_widget)


        # prediction progress bar
        self.pb_prediction = create_progressbar(
            max_value=20,
            text_format=f'Prediction ?/?'
        )
        self.pb_prediction.setToolTip('Show the progress of the prediction')

        # predict button
        predictions = QWidget()
        predictions.setLayout(QHBoxLayout())
        self.predict_button = QPushButton('Predict', self)
        self.predict_button.setEnabled(False)
        self.predict_button.setToolTip('Run the trained model on the images')

        predictions.layout().addWidget(QLabel(''))
        predictions.layout().addWidget(self.predict_button)

        # add to the group
        self.layout().addWidget(self.pb_prediction)
        self.layout().addWidget(predictions)

        # actions
        self.tiling_cbox.stateChanged.connect(self._update_tiles)

        if self.pred_status is not None and self.train_status is not None:
            # what to do when the buttons are clicked
            self.predict_button.clicked.connect(self._predict_button_clicked)

            # listening to the signals
            self.train_config_signal.events.is_3d.connect(self._set_3d)
            self.train_status.events.state.connect(self._update_button_from_train)
            self.pred_status.events.state.connect(self._update_button_from_pred)

            self.pred_status.events.sample_idx.connect(self._update_sample_idx)
            self.pred_status.events.max_samples.connect(self._update_max_sample)

    def _set_3d(self, state: bool) -> None:
        if self.pred_config_signal.tiled:
            self.tile_size_z.setEnabled(state)

    def _update_tiles(self, state: bool) -> None:
        self.pred_config_signal.tiled = state
        self.tile_size_xy.setEnabled(state)

        if self.train_config_signal.is_3d:
            self.tile_size_z.setEnabled(state)

    def _update_3d_tiles(self, state: bool) -> None:
        if self.pred_config_signal.tiled:
            self.tile_size_z.setEnabled(state)

    def _update_max_sample(self, max_sample: int) -> None:
        self.pb_prediction.setMaximum(max_sample)

    def _update_sample_idx(self, sample: int) -> None:
        self.pb_prediction.setValue(sample+1)
        self.pb_prediction.setFormat(f'Sample {sample+1}/{self.pred_status.max_samples}')

    def _predict_button_clicked(self) -> None:
        if self.pred_status is not None:
            if (
                self.pred_status.state == PredictionState.IDLE
                and self.train_status.state == TrainingState.DONE
            ):
                self.pred_status.state = PredictionState.PREDICTING
                self.predict_button.setText('Stop')

            elif self.pred_status.state == PredictionState.PREDICTING:
                self.pred_status.state = PredictionState.STOPPED
                self.predict_button.setText('Predict')

    def _update_button_from_train(self, state: TrainingState) -> None:
        if state == TrainingState.DONE:
            self.predict_button.setEnabled(True)
        else:
            self.predict_button.setEnabled(False)

    def _update_button_from_pred(self, state: PredictionState) -> None:
        if (
            state == PredictionState.DONE
            or state == PredictionState.CRASHED
        ):
            self.predict_button.setText('Predict')


if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # create signal
    train_signal = TrainingStatus()
    pred_signal = PredictionStatus()
    config_signal = PredictionSignal()
    
    # Instantiate widget
    widget = PredictionWidget(
        train_signal,
        pred_signal,
        config_signal
    )

    # Show the widget
    widget.show()

    # Run the application event loop
    sys.exit(app.exec_())