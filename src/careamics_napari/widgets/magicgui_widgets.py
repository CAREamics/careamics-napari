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


def two_layers_choice(names: list[str] = ["Train", "Val"]) -> Container:
    """Create a widget selecting two layers from the napari viewer.

    Parameters
    ----------
    names : list of str, default=["Train", "Val"]
        The names of the layers to select.

    Returns
    -------
    Container
        The widget selecting two layers from the napari viewer.

    Raises
    ------
    ImportError
        If napari is not installed.
    ValueError
        If the names list does not contain two strings only.
    ValueError
        If the names are the same.
    """
    if not _has_napari:
        raise ImportError("napari is not installed.")
    
    if len(names) != 2:
        raise ValueError("The names list must contain two strings only.")
    
    if names[0] == names[1]:
        raise ValueError("The names must be different.")
    
    img = layer_choice(annotation=Image, name=names[0])
    lbl = layer_choice(annotation=Image, name=names[1])

    return Container(widgets=[img, lbl])


def four_layers_choice() -> Container:
    """Create a widget to selecting four layers from the napari viewer.

    Returns
    -------
    Container
        The widget selecting four layers from the napari viewer.
    """
    # TODO can the text "TrainTarget" be made more friendly?
    img = two_layers_choice(annotation=Image, name=["Train", "TrainTarget"]) 
    lbl = two_layers_choice(annotation=Image, name=["Val", "ValTarget"])

    return img.extend(lbl)


@magic_factory(auto_call=True, Model={"mode": "r", "filter": "*.ckpt *.zip"})
def load_button(Model: Path):
    """A button to load model files.

    Parameters
    ----------
    Model : pathlib.Path
        The path to the model file.
    """
    pass
