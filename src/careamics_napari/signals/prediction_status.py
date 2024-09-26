from enum import Enum, IntEnum
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Union

from numpy.typing import NDArray

from psygnal import evented

if TYPE_CHECKING:
    from psygnal import SignalGroup, SignalInstance

    class PredictionStatusSignalGroup(SignalGroup):
        max_samples: SignalInstance
        sample_idx: SignalInstance
        state: SignalInstance


class PredictionUpdateType(str, Enum):
    MAX_SAMPLES = "max_samples"
    SAMPLE_IDX = "sample_idx"
    SAMPLE = "sample"
    STATE = "state"
    DEBUG = "debug message"
    EXCEPTION = "exception"


class PredictionState(IntEnum):
    IDLE = 0
    PREDICTING = 1
    DONE = 2
    STOPPED = 3
    CRASHED = 4


@dataclass
class PredictionUpdate:

    type: PredictionUpdateType
    value: Optional[Union[int, float, str, NDArray, PredictionState, Exception]] = None


@evented
@dataclass
class PredictionStatus:
    """Dataclass used to update the prediction UI with the current status and progress
    of the prediction process.
    """

    if TYPE_CHECKING:
        events: PredictionStatusSignalGroup

    max_samples: int = -1
    sample_idx: int = -1
    state: PredictionState = PredictionState.IDLE

    def update(self, new_update: PredictionUpdate) -> None:
        if (
            new_update.type != PredictionUpdateType.EXCEPTION
            and new_update.type != PredictionUpdateType.DEBUG
            and new_update.type != PredictionUpdateType.SAMPLE
        ):
            setattr(self, new_update.type.value, new_update.value)