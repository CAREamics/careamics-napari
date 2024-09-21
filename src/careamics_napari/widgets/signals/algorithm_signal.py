"""A signal representing the selected algorithm."""
from psygnal import evented
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from psygnal import SignalGroup, SignalInstance

    class ConfigurationSignalGroup(SignalGroup):
        algorithm: SignalInstance


@evented
@dataclass
class ConfigurationSignal:
    if TYPE_CHECKING:
        events: ConfigurationSignalGroup

    algorithm: str = ""
    use_channels: bool = False