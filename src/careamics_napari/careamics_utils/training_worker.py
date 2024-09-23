"""A thread worker function running CAREamics training."""
from typing import Generator
from queue import Queue
from threading import Thread

from napari.qt.threading import thread_worker

from careamics import CAREamist
from careamics.config.support import SupportedAlgorithm

from careamics_napari.careamics_utils.callback import UpdaterCallBack
from careamics_napari.careamics_utils.configuration import create_configuration
from careamics_napari.signals import (
    TrainingStatus, 
    Update,
    UpdateType,
    TrainingState, 
    ConfigurationSignal
)


# TODO register CAREamist to continue training and predict 
# TODO how to load pre-trained?
# TODO pass careamist here if it already exists?
@thread_worker
def train_worker(
    config_signal: ConfigurationSignal,
) -> Generator[Update, None, None]:

    # create update queue
    update_queue = Queue(10)

    # start training thread
    training = Thread(target=_train, args=(config_signal, update_queue))
    training.start()

    # loop looking for update events
    while True:
        update: Update = update_queue.get(block=True)

        if update.type == UpdateType.STATE:
            if update.value == TrainingState.DONE:
                yield update
                break
        else:
            yield update



def _train(config_signal: ConfigurationSignal, update_queue: Queue) -> None:
    
    # get configuration
    # config = create_configuration(config_signal)

    # # Create CAREamist
    # careamist = CAREamist(source=config, callbacks=[UpdaterCallBack(update_queue)])

    # # Register CAREamist
    # # yield careamist # TODO a bit hacky isn't it?

    # # Train CAREamist
    # train_data_target = None
    # val_data_target = None

    # if config_signal.load_from_disk:
    #     train_data = config_signal.path_train
    #     val_data = config_signal.path_val

    #     if config_signal.algorithm != SupportedAlgorithm.N2V:
    #         train_data_target = config_signal.path_train_target
    #         val_data_target = config_signal.path_val_target

    # else:
    #     train_data = config_signal.layer_train
    #     val_data = config_signal.layer_val

    #     if config_signal.algorithm != SupportedAlgorithm.N2V:
    #         train_data_target = config_signal.layer_train_target
    #         val_data_target = config_signal.layer_val_target

    # TODO add val percentage and val minimum
    try:
        # careamist.train(
        #     train_data=train_data, 
        #     val_data=val_data,
        #     train_data_target=train_data_target,
        #     val_data_target=val_data_target,
        # )
        update_queue.put(Update(UpdateType.MAX_EPOCH, 10_000 // 100))
        update_queue.put(Update(UpdateType.MAX_BATCH, 10_000))
        for i in range(10_000):
            if i % 100 == 0:
                update_queue.put(Update(UpdateType.EPOCH, i // 100))
                print(i)

            update_queue.put(Update(UpdateType.BATCH, i))


    except Exception as e:
        update_queue.put(Update(UpdateType.STATE, TrainingState.CRASHED))

    update_queue.put(Update(UpdateType.STATE, TrainingState.DONE))