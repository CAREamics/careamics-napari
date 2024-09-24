

from careamics import Configuration
from careamics.config import (
    create_care_configuration,
    create_n2n_configuration,
    create_n2v_configuration
)
from careamics.config.transformations import XYFlipModel, XYRandomRotate90Model
from careamics.config.support import SupportedAlgorithm

from careamics_napari.signals import TrainConfigurationSignal


def create_configuration(signal: TrainConfigurationSignal) -> Configuration:
    
    # experiment name
    if signal.experiment_name == "":
        experiment_name = f"{signal.algorithm}_{signal.axes}"
    else:
        experiment_name = signal.experiment_name

    if signal.is_3d:
        patches = (signal.patch_size_xy, signal.patch_size_xy, signal.patch_size_z)
    else:
        patches = (signal.patch_size_xy, signal.patch_size_xy)

    # model params
    model_params = {
        "depth": signal.depth,
        "num_channels_init": signal.size_conv_filters,
    }

    # augmentations
    augs = []
    if signal.x_flip or signal.y_flip:
        augs.append(XYFlipModel(flip_x = signal.x_flip, flip_y = signal.y_flip))

    if signal.rotations:
        augs.append(XYRandomRotate90Model())

    # create configuration
    if signal.algorithm == SupportedAlgorithm.N2V:
        return create_n2v_configuration(
            experiment_name=experiment_name,
            data_type="tiff" if signal.load_from_disk else "array",
            axes=signal.axes,
            patch_size=patches,
            batch_size=signal.batch_size,
            num_epochs=signal.n_epochs,
            n_channels=signal.n_channels_n2v,
            augmentations=augs,
            independent_channels=signal.independent_channels,
            use_n2v2=signal.use_n2v2,
            logger="tensorboard",
            model_params=model_params,
        )
    elif signal.algorithm == SupportedAlgorithm.N2N:
        return create_n2n_configuration(
            experiment_name=experiment_name,
            data_type="tiff" if signal.load_from_disk else "array",
            axes=signal.axes,
            patch_size=patches,
            batch_size=signal.batch_size,
            num_epochs=signal.n_epochs,
            n_channels_in=signal.n_channels_in_care,
            n_channels_out=signal.n_channels_out_care,
            augmentations=augs,
            independent_channels=signal.independent_channels,
            logger="tensorboard",
            model_params=model_params,
        )
    elif signal.algorithm == SupportedAlgorithm.CARE:
        return create_care_configuration(
            experiment_name=experiment_name,
            data_type="tiff" if signal.load_from_disk else "array",
            axes=signal.axes,
            patch_size=patches,
            batch_size=signal.batch_size,
            num_epochs=signal.n_epochs,
            n_channels_in=signal.n_channels_in_care,
            n_channels_out=signal.n_channels_out_care,
            augmentations=augs,
            independent_channels=signal.independent_channels,
            logger="tensorboard",
            model_params=model_params,
        )
    else:
        raise ValueError(f"Unsupported algorithm: {signal.algorithm}")
