
from careamics_napari.training_plugin import TrainPlugin
from careamics_napari.widgets.signals import ConfigurationSignal


def get_training_plugin():
    controller = TrainingController()

    return controller.get_widget()


class TrainingController:

    def __init__(self) -> None:

        # create signals
        config_signal = ConfigurationSignal()
        
        self.train_widget = TrainPlugin(config_signal)

    def get_widget(self) -> TrainPlugin:
        return self.train_widget
    