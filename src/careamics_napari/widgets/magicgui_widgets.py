from pathlib import Path
from typing import Any, Optional

from magicgui import magic_factory
from magicgui.widgets import Container, Widget, create_widget

# at run time
try:
    from napari import current_viewer
    from napari.layers import Image
except ImportError:
    _has_napari = False
else:
    _has_napari = True



def layer_choice(annotation: Optional[Any], **kwargs: Any) -> Widget:
    """Create a widget to select a layer from the napari viewer.

    Parameters
    ----------
    annotation : Any or None
        The annotation type to filter the layers.
    **kwargs : Any
        Additional keyword arguments to pass to the widget.

    Returns
    -------
    Widget
        The widget to select a layer from the napari viewer

    Raises
    ------
    ImportError
        If napari is not installed.
    """
    if not _has_napari:
        raise ImportError("napari is not installed.")

    widget: Widget = create_widget(annotation=annotation, **kwargs)
    widget.reset_choices()
    viewer = current_viewer()
    
    # connect to napari events
    viewer.layers.events.inserted.connect(widget.reset_choices)
    viewer.layers.events.removed.connect(widget.reset_choices)
    viewer.layers.events.changed.connect(widget.reset_choices)

    return widget


def two_layers_choice() -> Container:
    """Create a widget to select two layers from the napari viewer.

    Returns
    -------
    Container
        The widget to select two layers from the napari viewer.
    """
    if not _has_napari:
        raise ImportError("napari is not installed.")
    
    img = layer_choice(annotation=Image, name="Train")
    lbl = layer_choice(annotation=Image, name="Val")

    return Container(widgets=[img, lbl])


@magic_factory(auto_call=True, Model={"mode": "r", "filter": "*.ckpt *.zip"})
def load_button(Model: Path):
    """A button to load model files.

    Parameters
    ----------
    Model : pathlib.Path
        The path to the model file.
    """
    pass


@magic_factory(
    auto_call=True, use3d={"label": " ", "widget_type": "Checkbox", "visible": True}
)
def enable_3d(use_3d: bool = False) -> bool:
    """A checkbox to enable 3D mode.

    Parameters
    ----------
    use3d : bool, default=False
        Whether to enable 3D mode.

    Returns
    -------
    bool
        Whether 3D mode is enabled.
    """
    return use_3d
