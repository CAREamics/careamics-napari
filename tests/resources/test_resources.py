from pathlib import Path

from careamics_napari.resources import *


def test_gear():
    assert Path(ICON_GEAR).exists()
    assert type(ICON_GEAR) == str


def test_github():
    assert Path(ICON_GITHUB).exists()
    assert type(ICON_GITHUB) == str


def test_careamics():
    assert Path(ICON_CAREAMICS).exists()
    assert type(ICON_CAREAMICS) == str
