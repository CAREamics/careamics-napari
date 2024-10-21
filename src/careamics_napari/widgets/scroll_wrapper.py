"""Wrap a widget in a scroll area."""

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QScrollArea, QWidget


class ScrollWidgetWrapper(QScrollArea):
    """Wrap a widget in a scroll area.

    Parameters
    ----------
    widget : QWidget
        Widget to wrap.
    """

    def __init__(self, widget: QWidget) -> None:
        """Wrap a widget in a scroll area.

        Parameters
        ----------
        widget : QWidget
            Widget to wrap.
        """
        super().__init__()
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )  # ScrollBarAsNeeded
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(widget)
