

experiment_name: str,
data_type: Literal["array", "tiff", "custom"],
axes: str,
patch_size: list[int],
batch_size: int,
num_epochs: int,
augmentations: Optional[list[Union[XYFlipModel, XYRandomRotate90Model]]] = None,
independent_channels: bool = True,
use_n2v2: bool = False,
n_channels: int = 1,
roi_size: int = 11,
masked_pixel_percentage: float = 0.2,
struct_n2v_axis: Literal["horizontal", "vertical", "none"] = "none",
struct_n2v_span: int = 5,
logger: Literal["wandb", "tensorboard", "none"] = "none",
depth UNet
num_channels_init