"""A thread worker function running CAREamics training."""

from careamics import CAREamist, Configuration

from .._train_widget import TrainWidget
from .callback import UpdaterCallBack


# TODO pass object rather than widget?
# TODO how to load pre-trained?
def train_worker(train_widget: TrainWidget, config: Configuration) -> None:

    # Retrieve info from widget
    train_status = train_widget.get_training_status()  # TODO
    train_data = train_widget.get_training_data()
    val_data = train_widget.get_validation_data()

    # Create CAREamist
    # TODO if loading a pre-trained one, then how to update configuration?
    careamist = CAREamist(source=config, callbacks=[UpdaterCallBack(train_status)])

    # Train CAREamist
    careamist.train(train_data=train_data, val_data=val_data)
