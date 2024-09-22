from enum import IntEnum
from dataclasses import dataclass
from typing import TYPE_CHECKING

from psygnal import evented

if TYPE_CHECKING:
    from psygnal import SignalGroup, SignalInstance

    class TrainingStatusSignalGroup(SignalGroup):
        n_epochs: SignalInstance
        n_batches: SignalInstance
        epoch_idx: SignalInstance
        batch_idx: SignalInstance
        loss: SignalInstance
        val_loss: SignalInstance
        state: SignalInstance


class TrainingState(IntEnum):
    IDLE = 0
    TRAINING = 1
    DONE = 2
    STOPPED = 3
    CRASHED = 4


@evented
@dataclass
class TrainingStatus:
    if TYPE_CHECKING:
        events: TrainingStatusSignalGroup

    n_epochs: int = -1
    n_batches: int = -1
    epoch_idx: int = -1
    batch_idx: int = -1
    loss: float = -1
    val_loss: float = -1
    state: TrainingState = TrainingState.IDLE
