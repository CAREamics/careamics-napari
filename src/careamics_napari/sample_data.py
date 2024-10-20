"""Sample data for the careamics napari plugin."""

import numpy as np
from careamics.utils import get_careamics_home
from careamics_portfolio import PortfolioManager
from napari.types import LayerDataTuple
from napari.utils import notifications as ntf
from numpy.typing import NDArray
from tifffile import imread


def _load_sem_n2v() -> list[tuple[NDArray, dict[str, str]]]:
    """Download N2V SEM data.

    Returns
    -------
    list of (numpy.ndarray, dict)
        List of data and layer name.
    """
    files = PortfolioManager().denoising.N2V_SEM.download(path=get_careamics_home())

    img_train = imread(files[0])
    img_val = imread(files[1])

    return [(img_train, {"name": "train"}), (img_val, {"name": "val"})]


def _load_sem_n2n() -> list[tuple[NDArray, dict[str, str]]]:
    """Download N2N SEM data.

    Returns
    -------
    list of (numpy.ndarray, dict)
        List of data and layer name.
    """
    download = PortfolioManager().denoising.N2N_SEM.download(path=get_careamics_home())
    files = [f for f in download if f.endswith("tif")]
    files.sort()

    imgs_train = imread(files[1])
    img_train = imgs_train[2]
    img_target = imgs_train[3]

    return [(img_train, {"name": "train"}), (img_target, {"name": "target"})]


def _load_u2os_care() -> list[tuple[NDArray, dict[str, str]]]:
    """Download CARE U2OS data.

    Returns
    -------
    list of (numpy.ndarray, dict)
        List of data and layer name.
    """
    root_path = get_careamics_home()
    PortfolioManager().denoising.CARE_U2OS.download(root_path)

    # path to the training data
    root_path = root_path / "denoising-CARE_U2OS.unzip" / "data" / "U2OS"
    train_path = root_path / "train" / "low"
    target_path = root_path / "train" / "GT"

    # load the training data
    files_gt = list(target_path.glob("*.tif"))
    files_gt.sort()
    img_target = np.array([imread(f) for f in files_gt])

    files_low = list(train_path.glob("*.tif"))
    files_low.sort()
    img_train = np.array([imread(f) for f in files_low])

    return [(img_train, {"name": "train"}), (img_target, {"name": "target"})]


# def demo_files():
#     with cwd(get_default_path()):
#         # load sem validation
#         img = _load_sem()[1][0]

#         # create models folder if it doesn't already exist
#         model_path = Path('models', 'trained_sem_N2V2').absolute()
#         if not model_path.exists():
#             model_path.mkdir(parents=True)

#         # download sem model
#         model_zip_path = Path(model_path, 'trained_sem_N2V2.zip')
#         if not model_zip_path.exists():
#             # download and unzip data
#             urllib.request.urlretrieve(
#               'https://download.fht.org/jug/napari/trained_sem_N2V2.zip',
#                model_zip_path
#             )
#             with zipfile.ZipFile(model_zip_path, 'r') as zip_ref:
#                 zip_ref.extractall(model_path)

#         return img, Path(model_path, 'sem_N2V2.h5')


def n2v_sem_data() -> LayerDataTuple:
    """Load N2V SEM data.

    Returns
    -------
    LayerDataTuple
        Data and layer name.
    """
    ntf.show_info("Downloading data might take a few minutes.")
    return _load_sem_n2v()


def n2n_sem_data() -> LayerDataTuple:
    """Load N2N SEM data.

    Returns
    -------
    LayerDataTuple
        Data and layer name.
    """
    ntf.show_info("Downloading data might take a few minutes.")
    return _load_sem_n2n()


def care_u2os_data() -> LayerDataTuple:
    """Load CARE U2OS data.

    Returns
    -------
    LayerDataTuple
        Data and layer name.
    """
    ntf.show_info("Downloading data might take a few minutes.")
    return _load_u2os_care()


if __name__ == "__main__":

    import napari

    # create a Viewer
    viewer = napari.Viewer()

    # start UI
    napari.run()
