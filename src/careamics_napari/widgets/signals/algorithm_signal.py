"""A signal representing the selected algorithm."""
from psygnal import evented
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from psygnal import SignalGroup, SignalInstance

    class AlgorithmSignalGroup(SignalGroup):
        name: SignalInstance


@evented
@dataclass
class AlgorithmSignal:
    if TYPE_CHECKING:
        events: AlgorithmSignalGroup

    name: str = ""