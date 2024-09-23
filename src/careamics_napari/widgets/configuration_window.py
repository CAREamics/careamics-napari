"""A widget allowing setting advanced settings."""

from typing import Optional
from typing_extensions import Self

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QStackedWidget,
    QFormLayout,
    QCheckBox,
    QDialog,
    QLineEdit,
    QWidget,
    QPushButton,
)

from careamics.config.support import SupportedAlgorithm

from careamics_napari.widgets.signals import ConfigurationSignal
from careamics_napari.widgets import create_int_spinbox



# TODO missing:
# structn2v
# n2v masking parameters

# TODO should it be a singleton to make sure there only a single instance at a time?
# TODO add checkpointing parameters
# TODO add minimum percentage and minimum val data
# TODO add default values from the configuration_signal
class AdvancedConfigurationWindow(QDialog):

    def __init__(self, parent: QWidget, signal: Optional[ConfigurationSignal] = None):
        super().__init__(parent)
        
        self.configuration_signal = signal

        self.setLayout(QVBoxLayout())

        ##################
        # experiment name text box
        experiment_widget = QWidget()
        experiment_layout = QFormLayout()
        
        self.experiment_name = QLineEdit()
        self.experiment_name.setToolTip(
            "Name of the experiment. It will be used to save the model\n"
            "and the training history."
        )

        experiment_layout.addRow("Experiment name", self.experiment_name)
        experiment_widget.setLayout(experiment_layout)
        self.layout().addWidget(experiment_widget)

        ##################
        # augmentations group box, with x_flip, y_flip and rotations
        augmentations = QGroupBox("Augmentations")
        augmentations_layout = QFormLayout()

        self.x_flip = QCheckBox("X Flip")
        self.x_flip.setToolTip(
            "Check to add augmentation that flips the image\n"
            "along the x-axis"
        )
        self.y_flip = QCheckBox("Y Flip")
        self.y_flip.setToolTip(
            "Check to add augmentation that flips the image\n"
            "along the y-axis"
        )
        self.rotations = QCheckBox("90 Rotations")
        self.rotations.setToolTip(
            "Check to add augmentation that rotates the image\n"
            "in 90 degree increments in XY"
        )
        
        augmentations_layout.addRow(self.x_flip)
        augmentations_layout.addRow(self.y_flip)
        augmentations_layout.addRow(self.rotations)
        augmentations.setLayout(augmentations_layout)
        self.layout().addWidget(augmentations)
        
        ##################
        # channels
        self.channels = QGroupBox("Channels")
        channels_layout = QVBoxLayout()

        ind_channels_widget = QWidget()
        ind_channels_layout = QFormLayout()

        self.independent_channels = QCheckBox("Independent")
        self.independent_channels.setToolTip(
            "Check to treat the channels independently during\n"
            "training."
        )

        ind_channels_layout.addRow(self.independent_channels)
        ind_channels_widget.setLayout(ind_channels_layout)

        # n2v
        n2v_channels_widget = QWidget()
        n2v_channels_widget_layout = QFormLayout()

        self.n_channels = create_int_spinbox(1, 10, 1, 1)
        self.n_channels.setToolTip(
            "Number of channels in the input images"
        )
        
        n2v_channels_widget_layout.addRow("Channels", self.n_channels)
        n2v_channels_widget.setLayout(n2v_channels_widget_layout)

        # care/n2n
        care_channels_widget = QWidget()
        care_channels_widget_layout = QFormLayout()

        self.n_channels_in = create_int_spinbox(1, 10, 1, 1)
        self.n_channels_out = create_int_spinbox(1, 10, 1, 1)
        
        care_channels_widget_layout.addRow("Channels in", self.n_channels_in)
        care_channels_widget_layout.addRow("Channels out", self.n_channels_out)
        care_channels_widget.setLayout(care_channels_widget_layout)

        # stack n2v and care
        self.channels_stack = QStackedWidget()
        self.channels_stack.addWidget(n2v_channels_widget)
        self.channels_stack.addWidget(care_channels_widget)

        channels_layout.addWidget(ind_channels_widget)
        channels_layout.addWidget(self.channels_stack)
        self.channels.setLayout(channels_layout)
        self.layout().addWidget(self.channels)

        ##################
        # n2v2
        self.n2v2_widget = QGroupBox("N2V2")
        n2v2_layout = QFormLayout()

        self.use_n2v2 = QCheckBox("Use N2V2")
        self.use_n2v2.setToolTip(
            "Check to use N2V2 for training."
        )

        n2v2_layout.addRow(self.use_n2v2)
        self.n2v2_widget.setLayout(n2v2_layout)
        self.layout().addWidget(self.n2v2_widget)

        ##################
        # model params
        model_params = QGroupBox("UNet parameters")
        model_params_layout = QFormLayout()

        self.model_depth = create_int_spinbox(2, 5, 2, 1)
        self.model_depth.setToolTip(
            "Depth of the U-Net model."
        )
        self.size_conv_filters = create_int_spinbox(8, 1024, 32, 8, 8)
        self.size_conv_filters.setToolTip(
            "Number of convolutional filters in the first layer."
        )

        model_params_layout.addRow("Depth", self.model_depth)
        model_params_layout.addRow("N filters", self.size_conv_filters)
        model_params.setLayout(model_params_layout)
        self.layout().addWidget(model_params)

        ##################
        # save button
        button_widget = QWidget()
        button_widget.setLayout(QVBoxLayout())
        self.save_button = QPushButton("Save")
        self.save_button.setMaximumWidth(80)
        button_widget.layout().addWidget(self.save_button)
        button_widget.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(button_widget)

        ##################
        # actions and set defaults
        self.save_button.clicked.connect(self._save)

        if self.configuration_signal is not None:
            self.configuration_signal.events.use_channels.connect(
                self._update_to_channels
            )
            self._update_to_channels(self.configuration_signal.use_channels)

            self.configuration_signal.events.algorithm.connect(self._update_to_algorithm)
            self._update_to_algorithm(self.configuration_signal.algorithm)

    def _update_to_algorithm(self, name: str) -> None:
        if name == SupportedAlgorithm.N2V.value:
            self.n2v2_widget.setVisible(True)
            self.channels_stack.setCurrentIndex(0)
        else:
            self.n2v2_widget.setVisible(False)
            self.channels_stack.setCurrentIndex(1)


    def _update_to_channels(self, use_channels: bool) -> None:
        self.channels.setVisible(use_channels)

    def _save(self) -> None:
        """Save the configuration."""
        # Update the parameters
        if self.configuration_signal is not None:
            self.configuration_signal.experiment_name = self.experiment_name.text()
            self.configuration_signal.x_flip = self.x_flip.isChecked()
            self.configuration_signal.y_flip = self.y_flip.isChecked()
            self.configuration_signal.rotations = self.rotations.isChecked()
            self.configuration_signal.independent_channels = (
                self.independent_channels.isChecked()
            )
            self.configuration_signal.n_channels_n2v = self.n_channels.value()
            self.configuration_signal.n_channels_in_care = self.n_channels_in.value()
            self.configuration_signal.n_channels_out_care = self.n_channels_out.value()
            self.configuration_signal.use_n2v2 = self.use_n2v2.isChecked()
            self.configuration_signal.depth = self.model_depth.value()
            self.configuration_signal.size_conv_filters = self.size_conv_filters.value()

        self.close()
    


if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Signals
    myalgo = ConfigurationSignal(use_channels=False)

    # Instantiate widget
    widget = AdvancedConfigurationWindow(signal=myalgo)

    # Show the widget
    widget.show()

    # Run the application event loop
    sys.exit(app.exec_())