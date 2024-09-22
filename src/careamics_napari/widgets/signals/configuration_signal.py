"""A signal representing the selected algorithm."""
from psygnal import evented
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from psygnal import SignalGroup, SignalInstance

    class ConfigurationSignalGroup(SignalGroup):
        algorithm: SignalInstance
        use_channels: SignalInstance
        is_3d: SignalInstance



# TODO make sure defaults are used
@evented
@dataclass
class ConfigurationSignal:
    if TYPE_CHECKING:
        events: ConfigurationSignalGroup

    # signals used to change states across widgets
    algorithm: str = "n2v"
    use_channels: bool = False
    is_3d: bool = False

    # parameters set by widgets
    load_from_disk: bool = True

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
