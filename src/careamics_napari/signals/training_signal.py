from psygnal import evented
from dataclasses import dataclass
from typing import TYPE_CHECKING, Union
from pathlib import Path

from careamics.utils import get_careamics_home

if TYPE_CHECKING:
    from napari.layers import Image
    from psygnal import SignalGroup, SignalInstance

    class TrainingSignalGroup(SignalGroup):

        # only parameters that have observers are listed here
        algorithm: SignalInstance
        use_channels: SignalInstance
        is_3d: SignalInstance

try:
    from napari.layers import Image
except ImportError:
    _has_napari = False
else:
    _has_napari = True


# TODO make sure defaults are used
@evented
@dataclass
class TrainingSignal:
    if TYPE_CHECKING:
        events: TrainingSignalGroup

    # signals used to change states across widgets
    algorithm: str = "n2v"
    use_channels: bool = False
    is_3d: bool = False

    # parameters set by widgets for training
    work_dir: Union[str, Path] = get_careamics_home()
    load_from_disk: bool = True

    if _has_napari:
        layer_train: Image = None
        layer_train_target: Image = None
        layer_val: Image = None
        layer_val_target: Image = None

    path_train: str = ""
    path_train_target: str = ""
    path_val: str = ""
    path_val_target: str = ""

    axes: str = "YX"

    patch_size_xy: int = 64
    patch_size_z: int = 16
    n_epochs: int = 30
    batch_size: int = 16

    experiment_name = ""
    x_flip: bool = True
    y_flip: bool = True
    rotations: bool = True
    independent_channels: bool = True
    n_channels_n2v: int = 1
    n_channels_in_care: int = 1
    n_channels_out_care: int = 1
    use_n2v2: bool = False
    depth: int = 2
    size_conv_filters: int = 32
