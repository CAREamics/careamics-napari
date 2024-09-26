"""A thread worker function running CAREamics prediction."""
from typing import Generator, Optional
from queue import Queue
from threading import Thread

from napari.qt.threading import thread_worker
import napari.utils.notifications as ntf

from careamics import CAREamist

from careamics_napari.signals import (
    PredictionSignal,
    PredictionUpdate,
    PredictionUpdateType,
    PredictionState
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

    # start training thread
    training = Thread(
        target=_predict, 
        args=(
            careamist,
            config_signal, 
            update_queue,
        )
    )
    training.start()

    # look for updates
    while True:
        update: PredictionUpdate = update_queue.get(block=True)
        
        yield update

        if update.type == PredictionUpdateType.STATE:
            break

def _push_exception(queue: Queue, e: Exception) -> None:
    queue.put(PredictionUpdate(PredictionUpdateType.EXCEPTION, e))

def _predict(
    careamist: CAREamist,
    config_signal: PredictionSignal,
    update_queue: Queue,
) -> None:
    
    # Format data
    if config_signal.load_from_disk:

        if config_signal.path_pred == "":
            _push_exception(
                update_queue, 
                ValueError(
                    "Prediction data path is empty."
                )
            )
            return

        pred_data = config_signal.path_pred

    else:
        if config_signal.layer_pred is None:
            _push_exception(
                update_queue, 
                ValueError(
                    "Training data path is empty."
                )
            )

        pred_data = config_signal.layer_pred.data
     
    # Predict with CAREamist
    try:
        # careamist.train(
        #     train_source=train_data, 
        #     val_source=val_data,
        #     train_target=train_data_target,
        #     val_target=val_data_target,
        # )

        # # TODO can we use this to monkey patch the training process?
        import time
        update_queue.put(PredictionUpdate(PredictionUpdateType.MAX_SAMPLES, 1_000 // 10))
        for i in range(1_000):

            # if stopper.stop:
            #     update_queue.put(Update(UpdateType.STATE, TrainingState.STOPPED))
            #     break

            if i % 10 == 0:
                update_queue.put(PredictionUpdate(PredictionUpdateType.SAMPLE_IDX, i // 10))
                print(i)

      
            time.sleep(0.2) 

    except Exception as e:
        update_queue.put(
            PredictionUpdate(PredictionUpdateType.EXCEPTION, e)
        )

    update_queue.put(PredictionUpdate(PredictionUpdateType.STATE, PredictionState.DONE))