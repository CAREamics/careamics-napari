"""A widget used to select a path or layer for prediction."""

from typing import TYPE_CHECKING, Optional

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QFormLayout,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from typing_extensions import Self

from careamics_napari.signals import PredictionSignal
from careamics_napari.widgets import FolderWidget, layer_choice

if TYPE_CHECKING:
    import napari
    from napari.layers import Image

# at run time
try:
    import napari
    from napari.layers import Image
except ImportError:
    _has_napari = False
else:
    _has_napari = True


class PredictDataWidget(QTabWidget):
    """A widget offering to select a layer from napari or a path from disk.

    Parameters
    ----------
    prediction_signal : PredConfigurationSignal, default=None
        Signal to be updated with changed in widgets values.
    """

    def __init__(
        self: Self,
        prediction_signal: Optional[PredictionSignal] = None,
    ) -> None:
        """Initialize the widget.

        Parameters
        ----------
        prediction_signal : PredConfigurationSignal, default=None
            Signal to be updated with changed in widgets values.
        """
        super().__init__()

        self.config_signal = (
            PredictionSignal()  # type: ignore
            if prediction_signal is None
            else prediction_signal
        )

        # QTabs
        layer_tab = QWidget()
        layer_tab.setLayout(QVBoxLayout())
        disk_tab = QWidget()
        disk_tab.setLayout(QVBoxLayout())

        # add tabs
        self.addTab(layer_tab, "From layers")
        self.addTab(disk_tab, "From disk")
        self.setTabToolTip(0, "Use images from napari layers")
        self.setTabToolTip(1, "Use iamges saved on the disk")

        # set tabs
        self._set_layer_tab(layer_tab)
        self._set_disk_tab(disk_tab)

        # set actions
        if self.config_signal is not None:
            self.currentChanged.connect(self._set_data_source)
            self._set_data_source(self.currentIndex())

    def _set_layer_tab(
        self: Self,
        layer_tab: QWidget,
    ) -> None:
        """Set up the layer tab.

        Parameters
        ----------
        layer_tab : QWidget
            The layer tab.
        """
        if _has_napari and napari.current_viewer() is not None:
            form = QFormLayout()
            form.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
            form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
            form.setContentsMargins(12, 12, 0, 0)
            widget_layers = QWidget()
            widget_layers.setLayout(form)

            self.img_pred = layer_choice()
            form.addRow("Predict", self.img_pred.native)

            layer_tab.layout().addWidget(widget_layers)

            # connection actions for images
            self.img_pred.changed.connect(self._update_pred_layer)
            # to cover the case when image was loaded before the plugin
            if self.img_pred.value is not None:
                self._update_pred_layer(self.img_pred.value)

        else:
            # simply remove the tab
            self.removeTab(0)

    def _set_disk_tab(self: Self, disk_tab: QWidget) -> None:
        """Set up the disk tab.

        Parameters
        ----------
        disk_tab : QWidget
            The disk tab.
        """
        # disk tab
        buttons = QWidget()
        form = QFormLayout()
        form.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self.pred_images_folder = FolderWidget("Choose")
        form.addRow("Predict", self.pred_images_folder)

        self.pred_images_folder.setToolTip("Select a folder containing images.")

        # add actions
        self.pred_images_folder.get_text_widget().textChanged.connect(
            self._update_pred_folder
        )

        buttons.setLayout(form)
        disk_tab.layout().addWidget(buttons)

    def _set_data_source(self: Self, index: int) -> None:
        """Set the load_from_disk attribute of the signal based on the selected tab.

        Parameters
        ----------
        index : int
            Index of the selected tab.
        """
        if self.config_signal is not None:
            self.config_signal.load_from_disk = index == self.count() - 1

    def _update_pred_layer(self: Self, layer: Image) -> None:
        """Update the layer attribute of the signal.

        Parameters
        ----------
        layer : Image
            The selected layer.
        """
        if self.config_signal is not None:
            self.config_signal.layer_pred = layer

    def _update_pred_folder(self: Self, folder: str) -> None:
        """Update the path attribute of the signal.

        Parameters
        ----------
        folder : str
            The selected folder.
        """
        if self.config_signal.path_pred is not None:
            self.config_signal.path_pred = folder


if __name__ == "__main__":
    # from qtpy.QtWidgets import QApplication
    # import sys

    # # Create a QApplication instance
    # app = QApplication(sys.argv)

    # # create signal
    # signal = ConfigurationSignal()

    # # Instantiate widget
    # widget = DataSelectionWidget(signal, True)

    # # Show the widget
    # widget.show()

    # # Run the application event loop
    # sys.exit(app.exec_())

    import napari

    # create a Viewer
    viewer = napari.Viewer()

    # add napari-n2v plugin
    viewer.window.add_dock_widget(PredictDataWidget(PredictionSignal()))

    # add image to napari
    # viewer.add_image(data[0][0], name=data[0][1]['name'])

    # start UI
    napari.run()
