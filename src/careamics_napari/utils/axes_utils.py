"""Utilities to check axes validity."""

import warnings
from itertools import permutations

REF_AXES = "STCZYX"
"""References axes in CAREamics."""

NAPARI_AXES = "TSZYXC"  # TODO is this still true?
"""Axes used in Napari."""


def filter_dimensions(shape_length: int, is_3D: bool) -> list[str]:
    """Filter axes based on shape and dimensions.

    Parameters
    ----------
    shape_length : int
        Number of dimensions.
    is_3D : bool
        Whether the dimensions include Z.

    Returns
    -------
    list of str
        List of valid axes.
    """
    axes = list(REF_AXES)
    n = shape_length

    if not is_3D:  # if not 3D, remove it from the
        axes.remove("Z")

    if n > len(axes):
        warnings.warn("Data shape length is too large.", stacklevel=3)
        return []
    else:
        all_permutations = ["".join(p) for p in permutations(axes, n)]

        # X and Y must be in each permutation and contiguous (#FancyComments)
        all_permutations = [p for p in all_permutations if ("XY" in p) or ("YX" in p)]

        if is_3D:
            all_permutations = [p for p in all_permutations if "Z" in p]

        if len(all_permutations) == 0 and not is_3D:
            all_permutations = ["YX"]

        return all_permutations


# TODO should use function from CAREamics?
def are_axes_valid(axes: str) -> bool:
    """Check if axes are valid.

    Parameters
    ----------
    axes : str
        Axes to check.

    Returns
    -------
    bool
        Whether the axes are valid.
    """
    _axes = axes.upper()

    # length 0 and > 6
    if 0 > len(_axes) > 6:
        return False

    # all characters must be in REF_AXES = 'STZYXC'
    if not all(s in REF_AXES for s in _axes):
        return False

    # check for repeating characters
    for i, s in enumerate(_axes):
        if i != _axes.rfind(s):
            return False

    # prior: X and Y contiguous
    return ("XY" in _axes) or ("YX" in _axes)
