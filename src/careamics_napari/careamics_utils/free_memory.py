"""Utility to free GPU memory."""

import gc

from careamics import CAREamist
from torch.cuda import empty_cache


def free_memory(careamist: CAREamist) -> None:
    """Free memory from CAREamics instance.

    Parameters
    ----------
    careamist : CAREamist
        CAREamics instance.
    """
    if (
        careamist is not None
        and careamist.trainer is not None
        and careamist.trainer.model is not None
    ):
        careamist.trainer.model.cpu()
        del careamist.trainer.model
        del careamist.trainer
        del careamist

        gc.collect()
        empty_cache()
