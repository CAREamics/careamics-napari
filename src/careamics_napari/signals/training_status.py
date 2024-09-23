from enum import Enum, IntEnum
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Union

from psygnal import evented

if TYPE_CHECKING:
    from psygnal import SignalGroup, SignalInstance

    class TrainingStatusSignalGroup(SignalGroup):
        max_epochs: SignalInstance
        max_batches: SignalInstance
        epoch_idx: SignalInstance
        batch_idx: SignalInstance
        loss: SignalInstance
        val_loss: SignalInstance
        state: SignalInstance


class UpdateType(str, Enum):
    MAX_EPOCH = "max_epochs"
    EPOCH = "epoch_idx"
    MAX_BATCH = "max_batches"
    BATCH = "batch_idx"
    LOSS = "loss"
    VAL_LOSS = "val_loss"
    STATE = "state"


class TrainingState(IntEnum):
    IDLE = 0
    TRAINING = 1
    DONE = 2
    STOPPED = 3
    CRASHED = 4

@dataclass
class Stopper:
    stop: bool = False


@dataclass
class Update:

    type: UpdateType
    value: Optional[Union[int, float, TrainingState]] = None


@evented
@dataclass
class TrainingStatus:
    if TYPE_CHECKING:
        events: TrainingStatusSignalGroup

    max_epochs: int = -1
    max_batches: int = -1
    epoch_idx: int = -1
    batch_idx: int = -1
    loss: float = -1
    val_loss: float = -1
    state: TrainingState = TrainingState.IDLE

    def update(self, new_update: Update) -> None:
        setattr(self, new_update.type.value, new_update.value)