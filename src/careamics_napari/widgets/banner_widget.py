"""A banner widget with CAREamics logo, and links to Github and documentation."""

import webbrowser
from typing import Any
from typing_extensions import Self

from qtpy import QtCore, QtGui
from qtpy.QtGui import QCursor, QFont, QPixmap
from qtpy.QtWidgets import QHBoxLayout, QLabel, QPlainTextEdit, QVBoxLayout, QWidget

from careamics_napari.resources import ICON_GITHUB, ICON_CAREAMICS

DOC_LINK = 'https://careamics.github.io',
"""Link to the CAREamics documentation."""

GH_LINK = 'https://github.com/CAREamics/careamics'
"""Link to the CAREamics Github repository."""


def _create_link(link: str, text: str) -> QLabel:
    """Create link label.

    Parameters
    ----------
    link : str
        Link.
    text : str
        Text to display.

    Returns
    -------
    QLabel
        Link label.
    """
    label = QLabel()
    label.setContentsMargins(0, 5, 0, 5)

    label.setText(f"<a href='{link}' style='color:white'>{text}</a>")

    font = QFont()
    font.setPointSize(11)
    label.setFont(font)

    label.setOpenExternalLinks(True)

    return label


def _open_link(link: str):
    """Open link in browser.

    Parameters
    ----------
    link : str
        Link to open.
    """
    def link_opener(event: Any):
        webbrowser.open(link)

    return link_opener


class CAREamicsBanner(QWidget):
    """Banner widget with CAREamics logo, and links to Github and documentation.
    """

    def __init__(
        self: Self,
        title: str,
        short_desc: str,
    ) -> None:
        """Constructor.

        Parameters
        ----------
        title : str
            Title of the banner.
        short_desc : str
            Short description of the banner.
        """

        super().__init__()
        
        self.setMinimumSize(400, 200)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # logo
        icon = QPixmap(ICON_CAREAMICS)
        img_widget = QLabel()
        img_widget.setPixmap(icon)
        img_widget.setFixedSize(128, 128)

        # right panel
        right_layout = QVBoxLayout()
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        # title
        title = QLabel(title)
        title.setStyleSheet("font-weight: bold;")

        # description
        description_widget = QPlainTextEdit()
        description_widget.setReadOnly(True)
        description_widget.setPlainText(short_desc)
        description_widget.setFixedSize(200, 50)

        # bottom widget
        bottom_widget = QWidget()
        bottom_widget.setLayout(QHBoxLayout())

        # github logo
        gh_icon = QPixmap(ICON_GITHUB)
        gh_widget = QLabel()
        gh_widget.setPixmap(gh_icon)
        gh_widget.mousePressEvent = _open_link(GH_LINK)
        gh_widget.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        gh_widget.setToolTip("Report issues")

        # add widgets
        bottom_widget.layout().addWidget(_create_link(DOC_LINK, "Documentation"))
        bottom_widget.layout().addWidget(gh_widget)

        right_widget.layout().addWidget(title)
        right_widget.layout().addWidget(description_widget)
        right_widget.layout().addWidget(bottom_widget)

        # add widgets
        layout.addWidget(img_widget)
        layout.addWidget(right_widget)


if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    # Step 2: Create a QApplication instance
    app = QApplication(sys.argv)

    # Step 4: Instantiate your widget
    widget = CAREamicsBanner(
        "Test",
        "A test description for this widget."
    )

    # Step 5: Show the widget
    widget.show()

    # Step 6: Run the application event loop
    sys.exit(app.exec_())
