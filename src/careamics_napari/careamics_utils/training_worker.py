"""A thread worker function running CAREamics training."""
from typing import Generator

from napari.qt.threading import thread_worker

from careamics import CAREamist
from careamics.config.support import SupportedAlgorithm

from .callback import UpdaterCallBack
from .configuration import create_configuration
from careamics_napari.widgets.signals import (
    TrainingStatus, 
    TrainingState, 
    ConfigurationSignal
)


# TODO how to load pre-trained?
# TODO underusung thread_worker (no connection), why not a simple napari-independent thread?
# TODO pass careamist here if it already exists?
@thread_worker
def train_worker(
    config_signal: ConfigurationSignal,
    train_status: TrainingStatus,
) -> Generator[CAREamist, None, None]:

    # get configuration
    config = create_configuration(config_signal)

    # Create CAREamist
    careamist = CAREamist(source=config, callbacks=[UpdaterCallBack(train_status)])

    # Register CAREamist
    yield careamist # TODO a bit hacky isn't it?

    # Train CAREamist
    train_data_target = None
    val_data_target = None

    if config_signal.load_from_disk:
        train_data = config_signal.path_train
        val_data = config_signal.path_val

        if config_signal.algorithm != SupportedAlgorithm.N2V:
            train_data_target = config_signal.path_train_target
            val_data_target = config_signal.path_val_target

    else:
        train_data = config_signal.layer_train
        val_data = config_signal.layer_val

        if config_signal.algorithm != SupportedAlgorithm.N2V:
            train_data_target = config_signal.layer_train_target
            val_data_target = config_signal.layer_val_target

    # TODO add val percentage and val minimum
    try:
        # careamist.train(
        #     train_data=train_data, 
        #     val_data=val_data,
        #     train_data_target=train_data_target,
        #     val_data_target=val_data_target,
        # )
        for i in range(10_000):
            if i % 100 == 0:
                train_status.events.epoch_idx += 1 
                print(i)

            train_status.events.batch_idx += 1


    except Exception as e:
        train_status.events.state = TrainingState.CRASHED

    train_status.events.state = TrainingState.DONE