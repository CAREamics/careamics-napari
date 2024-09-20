
from careamics.config.support import SupportedAlgorithm

UNSUPPORTED = "I would prefer not to."

def get_available_algorithms() -> list[str]:
    return [
        get_friendly_name(algorithm) for algorithm in SupportedAlgorithm
        if get_friendly_name(algorithm) != UNSUPPORTED
    ] 


def get_friendly_name(algorithm: SupportedAlgorithm) -> str:
    if algorithm == SupportedAlgorithm.N2V:
        return "Noise2Void"
    elif algorithm == SupportedAlgorithm.CARE:
        return "CARE"
    elif algorithm == SupportedAlgorithm.N2N:
        return "Noise2Noise"
    else:
        return UNSUPPORTED