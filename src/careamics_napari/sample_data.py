
from tifffile import imread

from napari.types import LayerDataTuple
from napari.utils import notifications as ntf

from careamics.utils import get_careamics_home
from careamics_portfolio import PortfolioManager


def _load_sem():
    files = PortfolioManager().denoising.N2V_SEM.download(path=get_careamics_home())

    img_train = imread(files[0])
    img_val = imread(files[1])

    return [(img_train, {'name': 'train'}), (img_val, {'name': 'val'})]


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
#             urllib.request.urlretrieve('https://download.fht.org/jug/napari/trained_sem_N2V2.zip', model_zip_path)
#             with zipfile.ZipFile(model_zip_path, 'r') as zip_ref:
#                 zip_ref.extractall(model_path)

#         return img, Path(model_path, 'sem_N2V2.h5')



def n2v_sem_data() -> LayerDataTuple:
    ntf.show_info('Downloading data might take a few minutes.')
    return _load_sem()
