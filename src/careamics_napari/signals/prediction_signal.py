from psygnal import evented
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from napari.layers import Image

try:
    from napari.layers import Image
except ImportError:
    _has_napari = False
else:
    _has_napari = True


@evented
@dataclass
class PredictionSignal:

    load_from_disk: bool = True

    if _has_napari:
        layer_pred: Image = None

    path_pred: str = ""
    is_3d: bool = False
    tiled: bool = False
    tile_size_xy: int = 64
    tile_size_z: int = 8
    tile_overlap_xy: int = 48 # TODO currently fixed
    tile_overlap_z: int = 4 # TODO currently fixed