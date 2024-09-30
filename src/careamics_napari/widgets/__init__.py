"""Custom widgets used to build the plugins."""

__all__ = [
    "AxesWidget",
    "CAREamicsBanner",
    "FolderWidget",
    "create_gpu_label",
    "layer_choice",
    "load_button",
    "create_double_spinbox",
    "create_int_spinbox",
    "create_progressbar",
    "PowerOfTwoSpinBox",
    "ScrollWidgetWrapper",
    "TBPlotWidget",
    "AlgorithmSelectionWidget",
    "TrainDataWidget",
    "AdvancedConfigurationWindow",
    "ConfigurationWidget",
    "TrainingWidget",
    "TrainProgressWidget",
    "PredictDataWidget",
    "PredictionWidget",
    "SavingWidget",
]


from .algorithm_choice import AlgorithmSelectionWidget
from .axes_widget import AxesWidget
from .banner_widget import CAREamicsBanner
from .configuration_window import AdvancedConfigurationWindow
from .folder_widget import FolderWidget
from .gpu_widget import create_gpu_label
from .magicgui_widgets import layer_choice, load_button
from .predict_data_widget import PredictDataWidget
from .prediction_widget import PredictionWidget
from .qt_widgets import (
    PowerOfTwoSpinBox,
    create_double_spinbox,
    create_int_spinbox,
    create_progressbar,
)
from .saving_widget import SavingWidget
from .scroll_wrapper import ScrollWidgetWrapper
from .tbplot_widget import TBPlotWidget
from .train_data_widget import TrainDataWidget
from .train_progress_widget import TrainProgressWidget
from .training_configuration_widget import ConfigurationWidget
from .training_widget import TrainingWidget
