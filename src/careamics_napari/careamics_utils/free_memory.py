import gc

from torch.cuda import empty_cache
from careamics import CAREamist


def free_memory(careamist: CAREamist) -> None:
    """Free memory from CAREamics instance."""
    if careamist is not None:
        careamist.trainer.model.cpu()
        del careamist.trainer.model
        del careamist.trainer
        del careamist

        gc.collect()
        empty_cache()
