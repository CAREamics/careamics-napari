"""A widget allowing the creation of a CAREamics configuration."""

from typing import Optional

from qtpy import QtGui
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QPushButton,
    QFormLayout,
)

from careamics_napari.widgets.signals import AlgorithmSignal
from careamics_napari.resources import ICON_GEAR
from careamics_napari.widgets import (
    AxesWidget,
    create_int_spinbox,
    enable_3d
)


class ConfigurationWidget(QGroupBox):

    def __init__(self, signal: Optional[AlgorithmSignal] = None):
        super().__init__()

        self.setTitle("Training parameters")
        self.setMinimumWidth(100)

        # expert settings
        icon = QtGui.QIcon(ICON_GEAR)
        self.training_expert_btn = QPushButton(icon, '')
        self.training_expert_btn.setFixedSize(30, 30)
        self.training_expert_btn.setToolTip('Open the expert settings menu.')

        # axes
        self.axes_widget = AxesWidget()

        # others
        self.n_epochs_spin = create_int_spinbox(1, 1000, 30, tooltip='Number of epochs')
        self.n_epochs = self.n_epochs_spin.value()

        self.n_steps_spin = create_int_spinbox(1, 1000, 200, tooltip='Number of steps per epochs')
        self.n_steps = self.n_steps_spin.value()

        # batch size
        self.batch_size_spin = create_int_spinbox(1, 512, 16, 1)
        self.batch_size_spin.setToolTip('Number of patches per batch (decrease if GPU memory is insufficient)')

        # patch size
        self.patch_XY_spin = create_int_spinbox(16, 512, 64, 8, tooltip='Dimension of the patches in XY')

        # 3D checkbox
        self.enable_3d = enable_3d()
        self.enable_3d.native.setToolTip('Use a 3D network')
        self.patch_Z_spin = create_int_spinbox(16, 512, 16, 8, False, tooltip='Dimension of the patches in Z')

        formLayout = QFormLayout()
        formLayout.addRow(self.axes_widget.label.text(), self.axes_widget.text_field)
        formLayout.addRow('Enable 3D', self.enable_3d.native)
        formLayout.addRow('N epochs', self.n_epochs_spin)
        formLayout.addRow('N steps', self.n_steps_spin)
        formLayout.addRow('Batch size', self.batch_size_spin)
        formLayout.addRow('Patch XY', self.patch_XY_spin)
        formLayout.addRow('Patch Z', self.patch_Z_spin)
        formLayout.minimumSize()

        hlayout = QVBoxLayout()
        hlayout.addWidget(self.training_expert_btn, alignment=Qt.AlignRight | Qt.AlignVCenter)
        hlayout.addLayout(formLayout)

        self.setLayout(hlayout)
        self.layout().setContentsMargins(5, 20, 5, 10)


if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Signals
    myalgo = AlgorithmSignal()

    # Instantiate widget
    widget = ConfigurationWidget(myalgo)

    # Show the widget
    widget.show()

    # Run the application event loop
    sys.exit(app.exec_())