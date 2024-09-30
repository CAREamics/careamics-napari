import pytest

from careamics_napari.careamics_utils.configuration import create_configuration
from careamics_napari.signals import TrainingSignal


@pytest.mark.parametrize("algorithm", ["n2v", "care", "n2n"])
def test_creating_configuration(algorithm):
    """Test creating a configuration from a configuration signal state."""
    config_signal = TrainingSignal()  # default values
    config_signal.algorithm = algorithm

    # create configuration (runs through Pydantic validation)
    create_configuration(config_signal)
