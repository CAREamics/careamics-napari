"""A label indicating whether GPU is available to torch."""

from qtpy.QtWidgets import QLabel
from torch.cuda import is_available


def create_gpu_label() -> QLabel:
    """A label widget indicating whether GPU or CPU is available with torch.

    Returns
    -------
    QLabel
        GPU label widget.
    """
    if is_available():
        text = "GPU"
        color = "ADC2A9" # green
    else:
        text = "CPU"
        color = "FFDBA4" # yellow

    gpu_label = QLabel(text)
    font_color = gpu_label.palette().color(gpu_label.foregroundRole())

    gpu_label.setStyleSheet(
         f"font-weight: bold; color: #{color};"
    )
    gpu_label.setStyleSheet(
        f"""
            QLabel {{
                font-weight: bold; color: #{color};
            }}
            QToolTip {{
                color: {font_color};
            }}
        """
    )
    gpu_label.setToolTip(
        "Indicates whether PyTorch has access to a GPU. If your machine has GPU and "
        "this label indicates CPU, please check your PyTorch installation."
    )

    return gpu_label


if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    # Step 2: Create a QApplication instance
    app = QApplication(sys.argv)

    # Step 4: Instantiate your widget
    widget = create_gpu_label()

    # Step 5: Show the widget
    widget.show()

    # Step 6: Run the application event loop
    sys.exit(app.exec_())
