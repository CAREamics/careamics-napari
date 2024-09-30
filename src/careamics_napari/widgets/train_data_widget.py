from typing import TYPE_CHECKING, Optional

from qtpy.QtWidgets import (
    QFormLayout,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from typing_extensions import Self

from careamics_napari.signals import TrainingSignal
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


# TODO if user don't change the layers then they are None in the signal
class TrainDataWidget(QTabWidget):
    """A widget offering to select layers from napari or paths from disk."""

    def __init__(
        self: Self,
        signal: Optional[TrainingSignal] = None,
        use_target: bool = False,
    ) -> None:
        """Constructor.

        Parameters
        ----------
        signal : TrainConfigurationSignal, default=None
            Signal to be updated with changed in widgets values.
        use_target : bool, default=False
            Use train and validation target fields.
        """
        super().__init__()
        self.config_signal = signal
        self.use_target = use_target

        # QTabs
        layer_tab = QWidget()
        layer_tab.setLayout(QVBoxLayout())
        disk_tab = QWidget()
        disk_tab.setLayout(QVBoxLayout())

        # add tabs
        self.addTab(layer_tab, "From layers")
        self.addTab(disk_tab, "From disk")
        self.setTabToolTip(0, "Use images from napari layers")
        self.setTabToolTip(1, "Use patches saved on the disk")

        # set tabs
        self._set_layer_tab(layer_tab)
        self._set_disk_tab(disk_tab)

        # self.setMaximumHeight(400 if self.use_target else 200)

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

            self.img_train = layer_choice()
            self.img_train.native.setToolTip("Select a training layer.")

            self.img_val = layer_choice()
            self.img_train.native.setToolTip("Select a validation layer.")

            # connection actions for images
            self.img_train.changed.connect(self._update_train_layer)
            self.img_val.changed.connect(self._update_val_layer)

            if self.use_target:
                # get the target layers
                self.target_train = layer_choice()
                self.target_val = layer_choice()

                # tool tips
                self.target_train.native.setToolTip("Select a training target layer.")

                self.target_val.native.setToolTip("Select a validation target layer.")

                # connection actions for targets
                self.target_train.changed.connect(self._update_train_target_layer)
                self.target_val.changed.connect(self._update_val_target_layer)

                widget_layers.layout().addRow("Train", self.img_train.native)
                widget_layers.layout().addRow("Val", self.img_val.native)
                widget_layers.layout().addRow("Train target", self.target_train.native)
                widget_layers.layout().addRow("Val target", self.target_val.native)

            else:
                widget_layers.layout().addRow("Train", self.img_train.native)
                widget_layers.layout().addRow("Val", self.img_val.native)

            layer_tab.layout().addWidget(widget_layers)

        else:
            # simply remove the tab
            self.removeTab(0)

    def _set_disk_tab(self, disk_tab: QWidget) -> None:
        # disk tab
        buttons = QWidget()
        form = QFormLayout()
        # form.setContentsMargins(4, 0, 4, 0)
        # form.setSpacing(0)

        self.train_images_folder = FolderWidget("Choose")
        self.val_images_folder = FolderWidget("Choose")
        form.addRow("Train", self.train_images_folder)
        form.addRow("Val", self.val_images_folder)

        if self.use_target:
            self.train_target_folder = FolderWidget("Choose")
            self.val_target_folder = FolderWidget("Choose")

            form.addRow("Train target", self.train_target_folder)
            form.addRow("Val target", self.val_target_folder)

            self.train_target_folder.setToolTip(
                "Select a folder containing the training\n" "target."
            )
            self.val_target_folder.setToolTip(
                "Select a folder containing the validation\n" "target."
            )
            self.train_images_folder.setToolTip(
                "Select a folder containing the training\n" "images."
            )
            self.val_images_folder.setToolTip(
                "Select a folder containing the validation\n" "images."
            )

            # add actions to target
            self.train_target_folder.get_text_widget().textChanged.connect(
                self._update_train_target_folder
            )
            self.val_target_folder.get_text_widget().textChanged.connect(
                self._update_val_target_folder
            )

        else:
            self.train_images_folder.setToolTip(
                "Select a folder containing the training\n" "images."
            )
            self.val_images_folder.setToolTip(
                "Select a folder containing the validation\n"
                "images, if you select the same folder as\n"
                "for training, the validation patches will\n"
                "be extracted from the training data."
            )

        # add actions
        self.train_images_folder.get_text_widget().textChanged.connect(
            self._update_train_folder
        )
        self.val_images_folder.get_text_widget().textChanged.connect(
            self._update_val_folder
        )

        buttons.setLayout(form)
        disk_tab.layout().addWidget(buttons)

    def _set_data_source(self, index: int) -> None:
        if self.config_signal is not None:
            self.config_signal.load_from_disk = index == self.count() - 1

    def _update_train_layer(self, layer: Image) -> None:
        self.config_signal.layer_train = layer

    def _update_val_layer(self, layer: Image) -> None:
        self.config_signal.layer_val = layer

    def _update_train_target_layer(self, layer: Image) -> None:
        self.config_signal.layer_train_target = layer

    def _update_val_target_layer(self, layer: Image) -> None:
        self.config_signal.layer_val_target = layer

    def _update_train_folder(self, folder: str) -> None:
        self.config_signal.path_train = folder

    def _update_val_folder(self, folder: str) -> None:
        self.config_signal.path_val = folder

    def _update_train_target_folder(self, folder: str) -> None:
        self.config_signal.path_train_target = folder

    def _update_val_target_folder(self, folder: str) -> None:
        self.config_signal.path_val_target = folder


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
    viewer.window.add_dock_widget(TrainDataWidget(TrainingSignal(), True))

    # add image to napari
    # viewer.add_image(data[0][0], name=data[0][1]['name'])

    # start UI
    napari.run()
