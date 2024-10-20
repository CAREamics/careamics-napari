from pathlib import Path

from careamics_napari.resources import ICON_CAREAMICS, ICON_GEAR, ICON_GITHUB, ICON_TF


def test_gear():
    assert Path(ICON_GEAR).exists()
    assert isinstance(ICON_GEAR, str)


def test_github():
    assert Path(ICON_GITHUB).exists()
    assert isinstance(ICON_GITHUB, str)


def test_careamics():
    assert Path(ICON_CAREAMICS).exists()
    assert isinstance(ICON_CAREAMICS, str)


def test_tf():
    assert Path(ICON_TF).exists()
    assert isinstance(ICON_TF, str)
