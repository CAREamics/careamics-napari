
from typing import TYPE_CHECKING, Optional
from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QTabWidget,
)

from careamics_napari.widgets import (
    FolderWidget,
    two_layers_choice,

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


def create_tabs(napari_viewer: Optional[napari.Viewer] = None) -> QWidget:
    # QTabs
    tabs = QTabWidget()
    tab_layers = QWidget()
    tab_layers.setLayout(QVBoxLayout())
    tab_disk = QWidget()
    tab_disk.setLayout(QVBoxLayout())

    # add tabs
    tabs.addTab(tab_layers, 'From layers')
    tabs.addTab(tab_disk, 'From disk')
    tabs.setTabToolTip(0, 'Use images from napari layers')
    tabs.setTabToolTip(1, 'Use patches saved on the disk')
    tabs.setMaximumHeight(200)

    if _has_napari and napari_viewer is not None:
        layer_choice = two_layers_choice()
        tab_layers.layout().addWidget(layer_choice.native)

        # get the two layers
        img_train = layer_choice.Train
        img_val = layer_choice.Val

        img_train.native.setToolTip('Select a training layer.')
        img_val.native.setToolTip(
            'Select a validation layer (can\n'
            'be the same as for training, in\n'
            'which case validation patches will\n'
            'be extracted from the training data).'
        )
    else:
        tabs.removeTab(0)

    # disk tab
    train_images_folder = FolderWidget('Choose')
    val_images_folder = FolderWidget('Choose')

    buttons = QWidget()
    form = QFormLayout()

    form.addRow('Train', train_images_folder)
    form.addRow('Val', val_images_folder)

    buttons.setLayout(form)
    tab_disk.layout().addWidget(buttons)

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

    return tabs


if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Instantiate widget
    widget = create_tabs()

    # Show the widget
    widget.show()

    # Run the application event loop
    sys.exit(app.exec_())