"""Logo and icons."""

from pathlib import Path

ICON_GEAR = str(Path(Path(__file__).parent, "gear_16.png").absolute())
"""Path to the gear icon."""

ICON_GITHUB = str(Path(Path(__file__).parent, "GitHub-Mark-Light-32px.png").absolute())
"""Path to the GitHub icon."""

ICON_CAREAMICS = str(
    Path(Path(__file__).parent, "logo_careamics_v2_128.png").absolute()
)
"""Path to the CAREamics logo."""

ICON_TF = str(Path(Path(__file__).parent, "TF_White_Icon.png").absolute())
"""Path to the TensorFlow icon."""
