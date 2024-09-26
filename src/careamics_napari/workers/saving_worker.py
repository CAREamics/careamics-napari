"""A thread worker function running CAREamics prediction."""
from typing import Generator, Optional
from queue import Queue
from threading import Thread

from napari.qt.threading import thread_worker
import napari.utils.notifications as ntf

from careamics import CAREamist

from careamics_napari.signals import (
    SavingState,
    SavingStatus,
    SavingSignal,
    SavingUpdate,
    SavingUpdateType,
    ExportType,
    TrainingSignal
)


@thread_worker
def save_worker(
    careamist: CAREamist,
    training_signal: TrainingSignal,
    config_signal: SavingSignal,
) -> Generator[SavingUpdate, None, None]:

    dims = "3D" if training_signal.is_3d else "2D"
    name = f"{training_signal.algorithm}_{dims}_{training_signal.experiment_name}"

    # save model
    try:
        if config_signal.export_type == ExportType.BMZ:

            raise NotImplementedError("Export to BMZ not implemented yet.")
        
        else:
            name = name + ".ckpt"
            # TODO: should we reexport the model every time?
            careamist.trainer.save_checkpoint(
                config_signal.path_model / name,
            )

    except Exception as e:
        yield SavingUpdate(SavingUpdateType.EXCEPTION, e)

    yield SavingUpdate(SavingUpdateType.STATE, SavingState.DONE)