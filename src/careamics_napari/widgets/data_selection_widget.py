
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

if TYPE_CHECKING:
    import napari

# at run time
try:
    import napari
except ImportError:
    _has_napari = False
else:
    _has_napari = True


class DataSelectionWidget(QTabWidget):
    """A widget offering the select layers from napari or paths from disk.
    """

    def __init__(
            self: Self, 
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
        self.use_target = use_target
            
        # QTabs
        tab_layers = QWidget()
        tab_layers.setLayout(QVBoxLayout())
        tab_disk = QWidget()
        tab_disk.setLayout(QVBoxLayout())

        # add tabs
        self.addTab(tab_layers, 'From layers')
        self.addTab(tab_disk, 'From disk')
        self.setTabToolTip(0, 'Use images from napari layers')
        self.setTabToolTip(1, 'Use patches saved on the disk')

        if self.use_target:
            self.setMaximumHeight(400)
        else:
            self.setMaximumHeight(200)


        if _has_napari and napari_viewer is not None:

            if self.use_target:
                layer_choice = four_layers_choice()

                # get the layers
                img_train = layer_choice.Train
                target_train = layer_choice.TrainTarget
                img_val = layer_choice.Val
                target_val = layer_choice.ValTarget

                # tool tips
                img_train.native.setToolTip('Select a training layer.')
                target_train.native.setToolTip(
                    'Select a training target layer.'
                )

                img_train.native.setToolTip('Select a training layer.')
                target_val.native.setToolTip(
                    'Select a validation target layer.'
                )

            else:
                layer_choice = two_layers_choice()

                # get the layers
                img_train = layer_choice.Train
                img_val = layer_choice.Val

                img_train.native.setToolTip('Select a training layer.')
                img_val.native.setToolTip(
                    'Select a validation layer (can\n'
                    'be the same as for training, in\n'
                    'which case validation patches will\n'
                    'be extracted from the training data).'
                )

            
            tab_layers.layout().addWidget(layer_choice.native)
        else:
            self.removeTab(0)

        # disk tab
        buttons = QWidget()
        form = QFormLayout()

        train_images_folder = FolderWidget('Choose')
        val_images_folder = FolderWidget('Choose')
        form.addRow('Train', train_images_folder)
        form.addRow('Val', val_images_folder)

        if self.use_target:
            train_target_folder = FolderWidget('Choose')
            val_target_folder = FolderWidget('Choose')

            form.addRow('Train target', train_target_folder)
            form.addRow('Val target', val_target_folder)

            train_target_folder.setToolTip(
                'Select a folder containing the training\n'
                'target.'
            )
            val_target_folder.setToolTip(
                'Select a folder containing the validation\n'
                'target.'
            )
            train_images_folder.setToolTip(
                'Select a folder containing the training\n'
                'images.'
            )
            val_images_folder.setToolTip(
                'Select a folder containing the validation\n'
                'images.'
            )
        else:
            train_images_folder.setToolTip(
                'Select a folder containing the training\n'
                'images.'
            )
            val_images_folder.setToolTip(
                'Select a folder containing the validation\n'
                'images, if you select the same folder as\n'
                'for training, the validation patches will\n'
                'be extracted from the training data.'
            )

        buttons.setLayout(form)
        tab_disk.layout().addWidget(buttons)


if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Instantiate widget
    widget = DataSelectionWidget(True)

    # Show the widget
    widget.show()

    # Run the application event loop
    sys.exit(app.exec_())