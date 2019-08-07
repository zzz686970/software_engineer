"""calculate geo distance between two points

(xa, ya, za)
(xb, yb, zb)

"""
import numpy as np
from scipy.spatial import distance
def f1(a, b):
    return np.linalg.norm(a-b)

def f2(a, b):
    return distance.euclidean(a, b)


import numpy
import perfplot
from scipy.spatial import distance


def linalg_norm(data):
    a, b = data[0]
    return numpy.linalg.norm(a - b, axis=1)


def linalg_norm_T(data):
    a, b = data[1]
    return numpy.linalg.norm(a - b, axis=0)


def sqrt_sum(data):
    a, b = data[0]
    return numpy.sqrt(numpy.sum((a - b) ** 2, axis=1))


def sqrt_sum_T(data):
    a, b = data[1]
    return numpy.sqrt(numpy.sum((a - b) ** 2, axis=0))


def scipy_distance(data):
    a, b = data[0]
    return list(map(distance.euclidean, a, b))


def sqrt_einsum(data):
    a, b = data[0]
    a_min_b = a - b
    return numpy.sqrt(numpy.einsum("ij,ij->i", a_min_b, a_min_b))


def sqrt_einsum_T(data):
    a, b = data[1]
    a_min_b = a - b
    return numpy.sqrt(numpy.einsum("ij,ij->j", a_min_b, a_min_b))


def setup(n):
    a = numpy.random.rand(n, 3)
    b = numpy.random.rand(n, 3)
    out0 = numpy.array([a, b])
    out1 = numpy.array([a.T, b.T])
    return out0, out1

