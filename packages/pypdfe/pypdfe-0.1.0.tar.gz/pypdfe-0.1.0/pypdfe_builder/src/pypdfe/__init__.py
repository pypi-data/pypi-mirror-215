from __future__ import annotations
from ._core import __doc__, __version__, get_pdf
import numpy as np


def getpdf(data, return_size=10, debug=0):
    data = data.astype(float)
    x = np.zeros((return_size, data.shape[1]), dtype=float, order='F')
    pdf = np.zeros([return_size for _ in range(data.shape[1])], dtype=float, order='F')
    get_pdf(data, return_size, debug, x, pdf)
    return x, pdf


__all__ = ["__doc__", "__version__", "getpdf"]
