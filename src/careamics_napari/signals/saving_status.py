from enum import Enum, IntEnum
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Union

from numpy.typing import NDArray

from psygnal import evented

if TYPE_CHECKING:
    from psygnal import SignalGroup, SignalInstance

    class SavingSignalGroup(SignalGroup):
        state: SignalInstance


class SavingUpdateType(str, Enum):
    STATE = "state"
    DEBUG = "debug message"
    EXCEPTION = "exception"


class SavingState(IntEnum):
    IDLE = 0
    SAVING = 1
    CRASHED = 4


@dataclass
class SavingUpdate:

    type: SavingUpdateType
    value: Optional[Union[str, SavingState, Exception]] = None


@evented
@dataclass
class SavingStatus:
    """Dataclass used to update the saving UI with the current status and progress
    of the saving process.
    """

    if TYPE_CHECKING:
        events: SavingSignalGroup

    state: SavingState = SavingState.IDLE

    def update(self, new_update: SavingUpdate) -> None:
        setattr(self, new_update.type.value, new_update.value)