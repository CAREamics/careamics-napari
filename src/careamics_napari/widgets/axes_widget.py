"""Widget for specifying axes order."""

from enum import Enum
from typing import Any, Optional

from qtpy import QtGui
from qtpy.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget
from typing_extensions import Self

from careamics_napari.signals import TrainingSignal
from careamics_napari.utils import REF_AXES, are_axes_valid


class Highlight(Enum):
    """Axes highlight types."""

    VALID = 0
    """Valid axes."""

    UNRECOGNIZED = 1
    """Unrecognized axes."""

    NOT_ACCEPTED = 2
    """Axes not accepted."""


class LettersValidator(QtGui.QValidator):
    """Custom validator.

    Parameters
    ----------
    options : str
        Allowed characters.
    *args : Any
        Variable length argument list.
    **kwargs : Any
        Arbitrary keyword arguments.
    """

    def __init__(self: Self, options: str, *args: Any, **kwargs: Any) -> None:
        """Initialize the validator.

        Parameters
        ----------
        options : str
            Allowed characters.
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.
        """
        QtGui.QValidator.__init__(self, *args, **kwargs)
        self._options = options

    def validate(
        self: Self, value: str, pos: int
    ) -> tuple[QtGui.QValidator.State, str, int]:
        """Validate the input.

        Parameters
        ----------
        value : str
            Input value.
        pos : int
            Position of the cursor.

        Returns
        -------
        (QtGui.QValidator.State, str, int)
            Validation state, value, and position.
        """
        if len(value) > 0:
            if value[-1] in self._options:
                return QtGui.QValidator.Acceptable, value, pos
        else:
            if value == "":
                return QtGui.QValidator.Intermediate, value, pos
        return QtGui.QValidator.Invalid, value, pos


# TODO keep the validation?
# TODO is train layer selected, then show the orange and red, otherwise ignore?
class AxesWidget(QWidget):
    """A widget allowing users to specify axes.

    Parameters
    ----------
    n_axes : int, default=3
        Number of axes.
    is_3D : bool, default=False
        Whether the data is 3D.
    training_signal : TrainingSignal or None, default=None
        Signal holding all training parameters to be set by the user.
    """

    # TODO unused parameters
    def __init__(
        self, n_axes=3, is_3D=False, training_signal: Optional[TrainingSignal] = None
    ) -> None:
        """Initialize the widget.

        Parameters
        ----------
        n_axes : int, default=3
            Number of axes.
        is_3D : bool, default=False
            Whether the data is 3D.
        training_signal : TrainingSignal or None, default=None
            Signal holding all training parameters to be set by the user.
        """
        super().__init__()
        self.configuration_signal = training_signal

        # # max axes is 6
        # assert 0 < n_axes <= 6

        # self.n_axes = n_axes
        # self.is_3D = is_3D
        self.is_text_valid = True

        # QtPy
        self.setLayout(QHBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        # folder selection button
        self.label = QLabel("Axes")
        self.layout().addWidget(self.label)

        # text field
        self.text_field = QLineEdit(self.get_default_text())
        self.text_field.setMaxLength(6)
        self.text_field.setValidator(LettersValidator(REF_AXES))

        self.layout().addWidget(self.text_field)
        self.text_field.textChanged.connect(self._validate_text)
        self.text_field.setToolTip(
            "Enter the axes order as they are in your images, e.g. SZYX.\n"
            "Accepted axes are S(ample), T(ime), C(hannel), Z, Y, and X. Red\n"
            "color highlighting means that a character is not recognized,\n"
            "orange means that the axes order is not allowed. YX axes are\n"
            "mandatory."
        )

        # validate text
        self._validate_text()

        # set up signal handling when axes and 3D change
        self.text_field.textChanged.connect(self._axes_changed)

        # if self.configuration_signal is not None:
        #     self.configuration_signal.events.is_3d.connect(self.update_is_3D)

    def _axes_changed(self: Self) -> None:
        """Update the axes in the configuration signal if valid."""
        if self.configuration_signal is not None and self.is_text_valid:
            self.configuration_signal.use_channels = "C" in self.get_axes()
            self.configuration_signal.axes = self.get_axes()

    def _validate_text(self: Self) -> None:
        """Validate the text in the text field."""
        axes = self.get_axes()

        # change text color according to axes validation
        if are_axes_valid(axes):
            self._set_text_color(Highlight.VALID)
            # if axes.upper() in filter_dimensions(self.n_axes, self.is_3D):
            #     self._set_text_color(Highlight.VALID)
            # else:
            #     self._set_text_color(Highlight.NOT_ACCEPTED)
        else:
            self._set_text_color(Highlight.UNRECOGNIZED)

    def _set_text_color(self: Self, highlight: Highlight) -> None:
        """Set the text color according to the highlight type.

        Parameters
        ----------
        highlight : Highlight
            Highlight type.
        """
        self.is_text_valid = highlight == Highlight.VALID

        if highlight == Highlight.UNRECOGNIZED:
            self.text_field.setStyleSheet("color: red;")
        elif highlight == Highlight.NOT_ACCEPTED:
            self.text_field.setStyleSheet("color: orange;")
        else:  # VALID
            self.text_field.setStyleSheet("color: white;")

    def get_default_text(self: Self) -> str:
        """Return the default text.

        Returns
        -------
        str
            Default text.
        """
        # if self.is_3D:
        #     defaults = ["YX", "ZYX", "SZYX", "STZYX", "STCZYX"]
        # else:
        #     defaults = ["YX", "SYX", "STYX", "STCYX", "STC?YX"]

        # return defaults[self.n_axes - 2]
        return "YX"

    # def update_axes_number(self, n):
    #     self.n_axes = n
    #     self._validate_text()  # force new validation

    # def update_is_3D(self, is_3D):
    #     self.is_3D = is_3D
    #     self._validate_text()  # force new validation

    def get_axes(self: Self) -> str:
        """Return the axes order.

        Returns
        -------
        str
            Axes order.
        """
        return self.text_field.text()

    def is_valid(self: Self) -> bool:
        """Return whether the axes are valid.

        Returns
        -------
        bool
            Whether the axes are valid.
        """
        self._validate_text()  # probably unnecessary
        return self.is_text_valid

    def set_text_field(self: Self, text: str) -> None:
        """Set the text field.

        Parameters
        ----------
        text : str
            Text to set.
        """
        self.text_field.setText(text)


if __name__ == "__main__":
    import sys

    from qtpy.QtWidgets import QApplication

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Signals
    myalgo = TrainingSignal()  # type: ignore

    @myalgo.events.use_channels.connect
    def print_axes():
        """Print axes."""
        print(f"Use channels: {myalgo.use_channels}")

    # Instantiate widget
    widget = AxesWidget(training_signal=myalgo)

    # Show the widget
    widget.show()

    # Run the application event loop
    sys.exit(app.exec_())
