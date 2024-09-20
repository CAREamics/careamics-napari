
from typing import TYPE_CHECKING
from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QTabWidget,
)

from careamics_napari.widgets import (
    folder_widget,
    two_layers_choice,
    
)

if TYPE_CHECKING:
    from napari import Viewer

# at run time
try:
    import napari
except ImportError:
    _has_napari = False
else:
    _has_napari = True


def create_tabs(napari_viewer: Viewer) -> QWidget:
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

    self.layer_choice = two_layers_choice()
    self.img_train = self.layer_choice.Train
    self.img_val = self.layer_choice.Val
    tab_layers.layout().addWidget(self.layer_choice.native)
    self.img_train = ""
    self.img_val = ""
    self.img_train.native.setToolTip('Select an image for training')
    self.img_val.native.setToolTip('Select a n image for validation (can be the same as for training)')

    # disk tab
    self.train_images_folder = FolderWidget('Choose')
    self.val_images_folder = FolderWidget('Choose')

    buttons = QWidget()
    form = QFormLayout()

    form.addRow('Train', self.train_images_folder)
    form.addRow('Val', self.val_images_folder)

    buttons.setLayout(form)
    tab_disk.layout().addWidget(buttons)

    self.train_images_folder.setToolTip('Select a folder containing the training image')
    self.val_images_folder.setToolTip('Select a folder containing the validation images')
