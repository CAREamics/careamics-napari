"""A label indicating whether GPU is available to torch."""

from qtpy.QtWidgets import QLabel

from careamics_napari.utils.gpu_utils import is_gpu_available


def create_gpu_label() -> QLabel:
    """A label widget indicating whether GPU or CPU is available with torch.

    Returns
    -------
    QLabel
        GPU label widget.
    """
    if is_gpu_available():
        text = "GPU"
        color = "ADC2A9"  # green
    else:
        text = "CPU"
        color = "FFDBA4"  # yellow

    gpu_label = QLabel(text)
    font_color = gpu_label.palette().color(gpu_label.foregroundRole()).name()[1:]
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
        "Indicates whether PyTorch has access to a GPU.\n"
        "If your machine has GPU and this label indicates\n"
        "CPU, please check your PyTorch installation."
    )

    return gpu_label


if __name__ == "__main__":
    import sys

    from qtpy.QtWidgets import QApplication

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Instantiate widget
    widget = create_gpu_label()

    # Show the widget
    widget.show()

    # Run the application event loop
    sys.exit(app.exec_())
