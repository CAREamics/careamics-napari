"""A thread worker function running CAREamics prediction."""

from collections.abc import Generator
from queue import Queue
from threading import Thread
from typing import Optional, Union

from careamics import CAREamist
from napari.qt.threading import thread_worker

from careamics_napari.signals import (
    PredictionSignal,
    PredictionState,
    PredictionUpdate,
    PredictionUpdateType,
)


# TODO register CAREamist to continue training and predict
# TODO how to load pre-trained?
# TODO pass careamist here if it already exists?
@thread_worker
def predict_worker(
    careamist: CAREamist,
    config_signal: PredictionSignal,
    update_queue: Queue,
) -> Generator[PredictionUpdate, None, None]:
    """Model prediction worker.

    Parameters
    ----------
    careamist : CAREamist
        CAREamist instance.
    config_signal : PredictionSignal
        Prediction signal.
    update_queue : Queue
        Queue used to send updates to the UI.

    Yields
    ------
    Generator[PredictionUpdate, None, None]
        Updates.
    """
    # start training thread
    training = Thread(
        target=_predict,
        args=(
            careamist,
            config_signal,
            update_queue,
        ),
    )
    training.start()

    # look for updates
    while True:
        update: PredictionUpdate = update_queue.get(block=True)

        yield update

        if (
            update.type == PredictionUpdateType.STATE
            or update.type == PredictionUpdateType.EXCEPTION
        ):
            break


def _push_exception(queue: Queue, e: Exception) -> None:
    """Push an exception to the queue.

    Parameters
    ----------
    queue : Queue
        Queue.
    e : Exception
        Exception.
    """
    queue.put(PredictionUpdate(PredictionUpdateType.EXCEPTION, e))


def _predict(
    careamist: CAREamist,
    config_signal: PredictionSignal,
    update_queue: Queue,
) -> None:
    """Run the prediction.

    Parameters
    ----------
    careamist : CAREamist
        CAREamist instance.
    config_signal : PredictionSignal
        Prediction signal.
    update_queue : Queue
        Queue used to send updates to the UI.
    """
    # Format data
    if config_signal.load_from_disk:

        if config_signal.path_pred == "":
            _push_exception(update_queue, ValueError("Prediction data path is empty."))
            return

        pred_data = config_signal.path_pred

    else:
        if config_signal.layer_pred is None:
            _push_exception(
                update_queue, ValueError("Prediction layer has not been selected.")
            )

        elif config_signal.layer_pred.data is None:
            _push_exception(
                update_queue,
                ValueError(
                    f"Prediction layer {config_signal.layer_pred.name} is empty."
                ),
            )
        else:
            pred_data = config_signal.layer_pred.data

    # tiling
    if config_signal.tiled:
        if config_signal.is_3d:
            tile_size: Optional[Union[tuple[int, int, int], tuple[int, int]]] = (
                config_signal.tile_size_z,
                config_signal.tile_size_xy,
                config_signal.tile_size_xy,
            )
            tile_overlap: Optional[Union[tuple[int, int, int], tuple[int, int]]] = (
                config_signal.tile_overlap_z,
                config_signal.tile_overlap_xy,
                config_signal.tile_overlap_xy,
            )
        else:
            tile_size = (config_signal.tile_size_xy, config_signal.tile_size_xy)
            tile_overlap = (
                config_signal.tile_overlap_xy,
                config_signal.tile_overlap_xy,
            )
    else:
        tile_size = None
        tile_overlap = None

    # Predict with CAREamist
    try:
        result = careamist.predict(  # type: ignore
            pred_data,
            data_type="tiff" if config_signal.load_from_disk else "array",
            tile_size=tile_size,
            tile_overlap=tile_overlap,
        )

        update_queue.put(PredictionUpdate(PredictionUpdateType.SAMPLE, result))

        # # TODO can we use this to monkey patch the training process?
        # import time
        # update_queue.put(
        #   PredictionUpdate(PredictionUpdateType.MAX_SAMPLES, 1_000 // 10)
        # )
        # for i in range(1_000):

        #     # if stopper.stop:
        #     #     update_queue.put(Update(UpdateType.STATE, TrainingState.STOPPED))
        #     #     break

        #     if i % 10 == 0:
        #         update_queue.put(
        #              PredictionUpdate(PredictionUpdateType.SAMPLE_IDX, i // 10)
        #         )
        #         print(i)

        #     time.sleep(0.2)

    except Exception as e:
        update_queue.put(PredictionUpdate(PredictionUpdateType.EXCEPTION, e))
        return

    # signify end of prediction
    update_queue.put(PredictionUpdate(PredictionUpdateType.STATE, PredictionState.DONE))
