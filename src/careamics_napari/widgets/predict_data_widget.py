
from typing import TYPE_CHECKING, Optional
from typing_extensions import Self

from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QTabWidget,
)
from magicgui.widgets import Container

from careamics_napari.widgets import (
    FolderWidget,
    layer_choice
)
from careamics_napari.signals import PredictionSignal

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
    """

    def __init__(
            self: Self, 
            signal: Optional[PredictionSignal] = None,
    ) -> None:
        """Constructor.

        Parameters
        ----------
        signal : PredConfigurationSignal, default=None
            Signal to be updated with changed in widgets values.
        """
        super().__init__()
        self.config_signal = signal
            
        # QTabs
        layer_tab = QWidget()
        layer_tab.setLayout(QVBoxLayout())
        disk_tab = QWidget()
        disk_tab.setLayout(QVBoxLayout())

        # add tabs
        self.addTab(layer_tab, 'From layers')
        self.addTab(disk_tab, 'From disk')
        self.setTabToolTip(0, 'Use images from napari layers')
        self.setTabToolTip(1, 'Use iamges saved on the disk')

        # set tabs
        self._set_layer_tab(layer_tab)
        self._set_disk_tab(disk_tab)

        # set actions
        if self.config_signal is not None:
            self.currentChanged.connect(self._set_data_source)
            self._set_data_source(self.currentIndex())

    def _set_layer_tab(
            self, 
            layer_tab: QWidget, 
    ) -> None:
        if _has_napari and napari.current_viewer() is not None:
            widget_layers = QWidget()
            widget_layers.setLayout(QFormLayout())

            self.img_pred = layer_choice()
            widget_layers.layout().addRow("Predict", self.img_pred.native)

            layer_tab.layout().addWidget(widget_layers)

            # connection actions for images
            self.img_pred.changed.connect(self._update_pred_layer)

        else:
            # simply remove the tab
            self.removeTab(0)

    def _set_disk_tab(self, disk_tab: QWidget) -> None:
        # disk tab
        buttons = QWidget()
        form = QFormLayout()
        # form.setContentsMargins(4, 0, 4, 0)
        # form.setSpacing(0)

        self.pred_images_folder = FolderWidget('Choose')
        form.addRow('Predict', self.pred_images_folder)

        self.pred_images_folder.setToolTip(
            'Select a folder containing images.'
        )

        # add actions
        self.pred_images_folder.get_text_widget().textChanged.connect(
            self._update_pred_folder
        )

        buttons.setLayout(form)
        disk_tab.layout().addWidget(buttons)

    def _set_data_source(self, index: int) -> None:
        if self.config_signal is not None:
            self.config_signal.load_from_disk = index == self.count() - 1

    def _update_pred_layer(self, layer: Image) -> None:
        self.config_signal.layer_pred = layer
    
    def _update_pred_folder(self, folder: str) -> None:
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
    viewer.window.add_dock_widget(
        PredictDataWidget(
            PredictionSignal()
        )
    )

    # add image to napari
    # viewer.add_image(data[0][0], name=data[0][1]['name'])

    # start UI
    napari.run()