"""A widget allowing the creation of a CAREamics configuration."""

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
)

from careamics_napari.signals import TrainConfigurationSignal
from careamics_napari.resources import ICON_GEAR
from careamics_napari.widgets import (
    AxesWidget,
    create_int_spinbox,
    AdvancedConfigurationWindow
)


class ConfigurationWidget(QGroupBox):

    def __init__(self, signal: Optional[TrainConfigurationSignal] = None):
        super().__init__()

        self.configuration_signal = signal
        self.config_window = None

        self.setTitle("Training parameters")
        # self.setMinimumWidth(100)

        # expert settings
        icon = QtGui.QIcon(ICON_GEAR)
        self.training_expert_btn = QPushButton(icon, '')
        self.training_expert_btn.setFixedSize(35, 35)
        self.training_expert_btn.setToolTip('Open the expert settings menu.')     

        # 3D checkbox
        self.enable_3d = QCheckBox()
        self.enable_3d.setToolTip('Use a 3D network')
        self.patch_Z_spin = create_int_spinbox(16, 512, 16, 8, False, tooltip='Dimension of the patches in Z')

        # axes
        self.axes_widget = AxesWidget(signal=signal)

        # others
        self.n_epochs_spin = create_int_spinbox(1, 1000, 30, tooltip='Number of epochs')
        self.n_epochs = self.n_epochs_spin.value()

        # batch size
        self.batch_size_spin = create_int_spinbox(1, 512, 16, 1)
        self.batch_size_spin.setToolTip('Number of patches per batch (decrease if GPU memory is insufficient)')

        # patch size
        self.patch_XY_spin = create_int_spinbox(16, 512, 64, 8, tooltip='Dimension of the patches in XY')

        formLayout = QFormLayout()
        formLayout.addRow('Enable 3D', self.enable_3d)
        formLayout.addRow(self.axes_widget.label.text(), self.axes_widget.text_field)
        formLayout.addRow('N epochs', self.n_epochs_spin)
        formLayout.addRow('Batch size', self.batch_size_spin)
        formLayout.addRow('Patch XY', self.patch_XY_spin)
        formLayout.addRow('Patch Z', self.patch_Z_spin)
        formLayout.minimumSize()

        hlayout = QVBoxLayout()
        hlayout.addWidget(self.training_expert_btn, alignment=Qt.AlignRight | Qt.AlignVCenter)
        hlayout.addLayout(formLayout)

        self.setLayout(hlayout)
        self.layout().setContentsMargins(5, 20, 5, 10)

        # set actions
        self.training_expert_btn.clicked.connect(self._show_configuration_window)
        self.enable_3d.clicked.connect(self._enable_3d_changed)
        self.axes_widget.text_field.textChanged.connect(self._update_axes)
        self.n_epochs_spin.valueChanged.connect(self._update_n_epochs)
        self.batch_size_spin.valueChanged.connect(self._update_batch_size)
        self.patch_XY_spin.valueChanged.connect(self._update_patch_size_XY)
        self.patch_Z_spin.valueChanged.connect(self._update_patch_size_Z)

    def _show_configuration_window(self):
        if self.config_window is None or self.config_window.isHidden():
            self.config_window = (
                AdvancedConfigurationWindow(self, self.configuration_signal)
            )

            self.config_window.show()

    def _enable_3d_changed(self: Self, state: bool) -> None:
        self.patch_Z_spin.setVisible(state)
        
        if self.configuration_signal is not None:
            self.configuration_signal.is_3d = state

    def _update_axes(self: Self, axes: str) -> None:
        if self.configuration_signal is not None:
            self.configuration_signal.axes = axes

    def _update_n_epochs(self: Self, n_epochs: int) -> None:
        if self.configuration_signal is not None:
            self.configuration_signal.n_epochs = n_epochs

    def _update_batch_size(self: Self, batch_size: int) -> None:
        if self.configuration_signal is not None:
            self.configuration_signal.batch_size = batch_size

    def _update_patch_size_XY(self: Self, patch_size: int) -> None:
        if self.configuration_signal is not None:
            self.configuration_signal.patch_size_xy = patch_size
    
    def _update_patch_size_Z(self: Self, patch_size: int) -> None:
        if self.configuration_signal is not None:
            self.configuration_signal.patch_size_z = patch_size

if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Signals
    myalgo = TrainConfigurationSignal()

    # Instantiate widget
    widget = ConfigurationWidget(myalgo)

    # Show the widget
    widget.show()

    # Run the application event loop
    sys.exit(app.exec_())