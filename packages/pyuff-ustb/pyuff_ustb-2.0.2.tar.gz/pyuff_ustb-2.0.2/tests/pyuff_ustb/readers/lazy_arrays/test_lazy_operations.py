from contextlib import contextmanager

import numpy as np

from pyuff_ustb.readers import LazyArray, LazyScalar, Reader
from pyuff_ustb.readers.lazy_arrays.lazy_operations import (
    LazyOperation,
    LazyTranspose,
    apply_lazy_operations_on_data,
    apply_lazy_operations_on_index,
    apply_lazy_operations_on_shape,
)


class MockReader(Reader):
    def __init__(self, data: np.ndarray):
        self.data = data

    def append_path(self, path):
        if isinstance(path, str):
            path = (path,)
        return MockReader(self.path + tuple(path))

    def keys(self):
        return []

    @property
    def attrs(self):
        return {"complex": np.array(np.iscomplexobj(self.data))}

    @contextmanager
    def read(self):
        yield self.data


def test_lazy_transpose():
    arr = LazyArray(MockReader(np.array([[1], [2]])))
    assert arr.shape == (2, 1)
    assert arr.T.shape == (1, 2)

    np.testing.assert_array_equal(arr[...], np.array([[1], [2]]))
    np.testing.assert_array_equal(arr.T[...], np.array([[1, 2]]))


test_lazy_transpose()
