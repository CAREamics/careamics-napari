"""Custom widgets."""

from .axes_widget import AxesWidget
from .banner_widget import CAREamicsBanner
from .folder_widget import FolderWidget
from .gpu_widget import create_gpu_label
from .magicgui_widgets import (
    layer_choice, load_button
)
from .qt_widgets import (
    create_double_spinbox, 
    create_int_spinbox, 
    create_progressbar,
    PowerOfTwoSpinBox
)
from .scroll_wrapper import ScrollWidgetWrapper
from .tbplot_widget import TBPlotWidget
from .algorithm_choice import AlgorithmChoiceWidget
from .train_data_widget import TrainDataWidget
from .configuration_window import AdvancedConfigurationWindow
from .training_configuration_widget import ConfigurationWidget
from .training_widget import TrainingWidget
from .train_progress_widget import TrainProgressWidget
from .predict_data_widget import PredictDataWidget
from .prediction_widget import PredictionWidget
from .saving_widget import SavingWidget
