import numpy as np

from careamics_napari.sample_data import n2n_sem_data, n2v_sem_data


def test_n2v_sem_data():
    data = n2v_sem_data()
    assert len(data) == 2
    assert all(isinstance(d, np.ndarray) for d, _ in data)


def test_n2n_sem_data():
    data = n2n_sem_data()
    assert len(data) == 2
    assert all(isinstance(d, np.ndarray) for d, _ in data)
