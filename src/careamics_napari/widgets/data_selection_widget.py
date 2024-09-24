
from typing import TYPE_CHECKING, Optional
from typing_extensions import Self

from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QTabWidget,
)

from careamics_napari.widgets import (
    FolderWidget,
    two_layers_choice,
    four_layers_choice
)
from careamics_napari.signals import ConfigurationSignal

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


class DataSelectionWidget(QTabWidget):
    """A widget offering to select layers from napari or paths from disk.
    """

    def __init__(
            self: Self, 
            signal: Optional[ConfigurationSignal] = None,
            use_target: bool = False, 
            napari_viewer: Optional[napari.Viewer] = None
    ) -> None:
        """Constructor.

        Parameters
        ----------
        use_target : bool, default=False
            Use train and validation target fields.
        napari_viewer : napari.Viewer or None, default=None
            Napari viewer.
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
        self.addTab(layer_tab, 'From layers')
        self.addTab(disk_tab, 'From disk')
        self.setTabToolTip(0, 'Use images from napari layers')
        self.setTabToolTip(1, 'Use patches saved on the disk')

        # set tabs
        self._set_layer_tab(layer_tab, napari_viewer)
        self._set_disk_tab(disk_tab)

        # set actions
        if self.config_signal is not None:
            self.currentChanged.connect(self._set_data_source)
            self._set_data_source(self.currentIndex())

    def _set_layer_tab(
            self, 
            layer_tab: QWidget, 
            napari_viewer: Optional[napari.Viewer]
    ) -> None:

        if self.use_target:
            self.setMaximumHeight(400)
        else:
            self.setMaximumHeight(200)


        if _has_napari and napari_viewer is not None:

            if self.use_target:
                layer_choice = four_layers_choice()

                # get the layers
                self.img_train = layer_choice.Train
                self.target_train = layer_choice.TrainTarget
                self.img_val = layer_choice.Val
                self.target_val = layer_choice.ValTarget

                # tool tips
                self.img_train.native.setToolTip('Select a training layer.')
                self.target_train.native.setToolTip(
                    'Select a training target layer.'
                )

                self.img_train.native.setToolTip('Select a training layer.')
                self.target_val.native.setToolTip(
                    'Select a validation target layer.'
                )

                # connection actions for targets
                self.target_train.changed.connect(self._update_train_target_layer)
                self.target_val.changed.connect(self._update_val_target_layer)

            else:
                layer_choice = two_layers_choice()

                # get the layers
                self.img_train = layer_choice.Train
                self.img_val = layer_choice.Val

                self.img_train.native.setToolTip('Select a training layer.')
                self.img_val.native.setToolTip(
                    'Select a validation layer (can\n'
                    'be the same as for training, in\n'
                    'which case validation patches will\n'
                    'be extracted from the training data).'
                )

            # connection actions for images
            self.img_train.changed.connect(self._update_train_layer)
            self.img_val.changed.connect(self._update_val_layer)

            
            layer_tab.layout().addWidget(layer_choice.native)

        else:
            self.removeTab(0)

    def _set_disk_tab(self, disk_tab: QWidget) -> None:
        # disk tab
        buttons = QWidget()
        form = QFormLayout()
        # form.setContentsMargins(4, 0, 4, 0)
        # form.setSpacing(0)

        self.train_images_folder = FolderWidget('Choose')
        self.val_images_folder = FolderWidget('Choose')
        form.addRow('Train', self.train_images_folder)
        form.addRow('Val', self.val_images_folder)

        if self.use_target:
            self.train_target_folder = FolderWidget('Choose')
            self.val_target_folder = FolderWidget('Choose')

            form.addRow('Train target', self.train_target_folder)
            form.addRow('Val target', self.val_target_folder)

            self.train_target_folder.setToolTip(
                'Select a folder containing the training\n'
                'target.'
            )
            self.val_target_folder.setToolTip(
                'Select a folder containing the validation\n'
                'target.'
            )
            self.train_images_folder.setToolTip(
                'Select a folder containing the training\n'
                'images.'
            )
            self.val_images_folder.setToolTip(
                'Select a folder containing the validation\n'
                'images.'
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
                'Select a folder containing the training\n'
                'images.'
            )
            self.val_images_folder.setToolTip(
                'Select a folder containing the validation\n'
                'images, if you select the same folder as\n'
                'for training, the validation patches will\n'
                'be extracted from the training data.'
            )

        # add actions
        self.train_images_folder.get_text_widget().textChanged.connect(self._update_train_folder)
        self.val_images_folder.get_text_widget().textChanged.connect(self._update_val_folder)


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
    viewer.window.add_dock_widget(DataSelectionWidget(
        ConfigurationSignal(), True, viewer
    ))

    # add image to napari
    # viewer.add_image(data[0][0], name=data[0][1]['name'])

    # start UI
    napari.run()