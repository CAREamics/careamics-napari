
from __future__ import annotations

from pathlib import Path
from typing import Union

from dataclasses import dataclass
from enum import Enum

class ExportType(str, Enum):
    
    BMZ = "Bioimage.io"
    CKPT = "Checkpoint"

    @classmethod
    def list(cls) -> list[str]:
        return list(map(lambda c: c.value, cls))
    
@dataclass
class SavingSignal:

    path_model: Union[str, Path] = ""
    export_type: ExportType = ExportType.BMZ

