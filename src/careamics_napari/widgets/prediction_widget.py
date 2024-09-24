

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

from careamics_napari.widgets import create_int_spinbox, create_progressbar
from careamics_napari.signals import TrainConfigurationSignal

class PredictionWidget(QGroupBox):

    def __init__(
            self: Self,
            config_signal: Optional[TrainConfigurationSignal] = None
    ) -> None:
        
        self.config_signal = config_signal
        
        self.setTitle("Prediction")
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(20, 20, 20, 0)

        # checkbox
        self.tiling_cbox = QCheckBox('Tile prediction')
        self.tiling_cbox.setToolTip(
            'Select to predict the image by tiles, allowing '
            'to predict on large images.'
        )
        self.layout().addWidget(self.tiling_cbox)

        # tiling spinbox
        self.tiling_spin = create_int_spinbox(1, 1000, 4, tooltip='Minimum number of tiles to use.')
        self.tiling_spin.setEnabled(False)

        tiling_form = QFormLayout()
        tiling_form.addRow('Number of tiles', self.tiling_spin)
        tiling_widget = QWidget()
        tiling_widget.setLayout(tiling_form)
        self.layout().addWidget(tiling_widget)

        # prediction progress bar
        self.pb_prediction = create_progressbar(max_value=20,
                                                text_format=f'Prediction ?/?')
        self.pb_prediction.setToolTip('Show the progress of the prediction')

        # predict button
        predictions = QWidget()
        predictions.setLayout(QHBoxLayout())
        self.predict_button = QPushButton('', self)
        self.predict_button.setEnabled(False)
        self.predict_button.setToolTip('Run the trained model on the images')

        predictions.layout().addWidget(QLabel(''))
        predictions.layout().addWidget(self.predict_button)

        # add to the group
        self.layout().addWidget(self.pb_prediction)
        self.layout().addWidget(predictions)
