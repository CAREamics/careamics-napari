from pathlib import Path

from magicgui.experimental import guiclass
from pydantic import BaseModel, Field


@guiclass
class Config(BaseModel):
    input_dir: Path = ""
    some_string: str = Field(default="dummy")
    some_number: float = 0.5


if __name__ == "__main__":

    obj = Config(input_dir="", some_string="dfs", some_number=4)
    obj.gui.show()
