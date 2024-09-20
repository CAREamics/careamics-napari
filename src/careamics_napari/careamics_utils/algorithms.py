
from careamics.config.support import SupportedAlgorithm

UNSUPPORTED = "I would prefer not to."

def get_available_algorithms() -> list[str]:
    """Return the available algorithms friendly names.

    Returns
    -------
    list of str
        A list of available algorithms.
    """
    return [
        get_friendly_name(algorithm) for algorithm in SupportedAlgorithm
        if get_friendly_name(algorithm) != UNSUPPORTED
    ] 


def get_friendly_name(algorithm: SupportedAlgorithm) -> str:
    """Return the friendly name of an algorithm.

    Parameters
    ----------
    algorithm : SupportedAlgorithm
        Algorithm.

    Returns
    -------
    str
        Friendly name.
    """
    if algorithm == SupportedAlgorithm.N2V:
        return "Noise2Void"
    elif algorithm == SupportedAlgorithm.CARE:
        return "CARE"
    elif algorithm == SupportedAlgorithm.N2N:
        return "Noise2Noise"
    else:
        return UNSUPPORTED
    

def get_algorithm(friendly_name: str) -> str:
    """Return the algorithm corresponding to the friendly name.

    Parameters
    ----------
    friendly_name : str
        Friendly name.

    Returns
    -------
    str
        Algorithm.
    """
    if friendly_name == "Noise2Void":
        return SupportedAlgorithm.N2V.value
    elif friendly_name == "CARE":
        return SupportedAlgorithm.CARE.value
    elif friendly_name == "Noise2Noise":
        return SupportedAlgorithm.N2N.value
    else:
        raise ValueError(f"Unsupported algorithm: {friendly_name}")