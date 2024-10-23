"""Utilities to test GPU availability with torch."""

import os
import platform

from torch import backends, cuda


def is_gpu_available() -> bool:
    """Check if GPU is available with torch.

    Returns
    -------
    bool
        True if GPU is available, False otherwise.
    """
    if platform.system() == "Darwin":
        # adapted from Lightning
        # pytorch-lightning/src/lightning/fabric/accelerators/mps.py
        mps_disabled = os.getenv("DISABLE_MPS", "0") == "1"
        return (
            not mps_disabled
            and backends.mps.is_available()
            and platform.processor() in ("arm", "arm64")
        )
    else:
        return cuda.is_available()
