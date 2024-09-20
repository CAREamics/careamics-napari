from qtpy.QtWidgets import QLabel
from torch.cuda import is_available


def create_gpu_label_widget() -> QLabel:
    """A label widget indicating whether GPU or CPU is available with torch.

    Returns
    -------
    QLabel
        GPU label widget.
    """
    if is_available():
        text = "GPU"
        color = "ADC2A9"
    else:
        text = "CPU"
        color = "FFDBA4"

    gpu_label = QLabel(text)
    gpu_label.setStyleSheet(f"font-weight: bold; color: #{color};")
    gpu_label.setToolTip("Indicates whether DenoiSeg will run on GPU or CPU")

    return gpu_label
