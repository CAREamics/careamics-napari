"""A widget allowing setting advanced settings."""

from typing import Optional
from typing_extensions import Self

from qtpy import QtGui
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QPushButton,
    QFormLayout,
    QCheckBox,
    QDialog,
    QLineEdit
)

from careamics_napari.widgets.signals import ConfigurationSignal


"""
experiment_name: str,
n_channels: int = 1,
independent_channels: bool = True,
augmentations: Optional[list[Union[XYFlipModel, XYRandomRotate90Model]]] = None,
use_n2v2: bool = False,
roi_size: int = 11,
masked_pixel_percentage: float = 0.2,
struct_n2v_axis: Literal["horizontal", "vertical", "none"] = "none",
struct_n2v_span: int = 5,
depth UNet
num_channels_init
"""

class ConfigurationWidget(QDialog):

    def __init__(self, signal: Optional[ConfigurationSignal] = None):
        
        super().__init__()

        self.configuration_signal = signal

        # experiment name text box
        self.experiment_name = QLineEdit()


        formLayout = QFormLayout()