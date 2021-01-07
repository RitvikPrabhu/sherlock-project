import unittest
from unittest import TestCase
from scipy.stats import skew, kurtosis
from array import array
from sherlock.features.stats_helper import compute_stats, mode
from numpy.testing import assert_array_almost_equal
import numpy as np
from timeit import timeit
import statistics as statistics


def old_stats(values):
    _mean = np.mean(values)
    _variance = np.var(values)
    _skew = skew(values)
    _kurtosis = kurtosis(values)
    _min = np.min(values)
    _max = np.max(values)
    _sum = np.sum(values)

    return _mean, _variance, _skew, _kurtosis, _min, _max, _sum


class Test(TestCase):

    def test_custom_stats(self):
        all_values = [array('i', [1, 1, 1, 1, 1, 1, 1]),
                      array('i', [1, 0, 0, 0, 1]),
                      array('i', [0, 1, 1, 1, 0]),
                      array('i', [2, 1, 1, 1, 2]),
                      array('i', [2, 0, 0, 0, 1]),
                      array('i', [1, 0, 0, 0, 0]),
                      array('i', [1, 0, 0, 0, 1]),
                      array('i', [1, 1, 1, 2, 1]),
                      array('i', [1, 0, 0, 2, 1]),
                      array('i', [0, 1, 1, 0, 0]),
                      array('i', [0, 0, 0, 1, 0]),
                      array('i', [1, 0, 0, 0, 1]),
                      array('i', [0, 1, 1, 0, 0]),
                      array('i', [1, 0, 0, 0, 0]),
                      array('i', [4, 1, 1, 0, 1]),
                      array('i', [0, 1, 1, 1, 1]),
                      array('i', [1, 1, 1, 1, 2]),
                      array('i', [8, 0, 0, 3, 3]),
                      array('i', [1, 0, 0, 1, 0]),
                      array('i', [1, 0, 0, 0, 0]),
                      array('i', [2, 2, 2, 1, 2]),
                      array('i', [1, 0, 0, 0, 1]),
                      array('i', [6, 2, 2, 1, 0]),
                      array('i', [1, 2, 2, 1, 0]),
                      array('i', [1, 0, 0, 2, 0]),
                      array('i', [4, 2, 2, 1, 3]),
                      array('i', [3, 2, 2, 1, 1]),
                      array('i', [4, 4, 4, 2, 1]),
                      array('i', [1, 1, 1, 1, 0]),
                      array('i', [0, 0, 0, 0, 1])]

        for values in all_values:
            _mean, _variance, _skew, _kurtosis, _min, _max, _sum = old_stats(values)

            _mean2, _variance2, _skew2, _kurtosis2, _min2, _max2, _sum2 = compute_stats(values)

            assert_array_almost_equal(_mean, _mean2, err_msg=f'mismatch for values {values}')
            assert_array_almost_equal(_variance, _variance2, err_msg=f'mismatch for values {values}')
            assert_array_almost_equal(_skew, _skew2, err_msg=f'mismatch for values {values}')
            assert_array_almost_equal(_kurtosis, _kurtosis2, err_msg=f'mismatch for values {values}')
            assert_array_almost_equal(_min, _min2, err_msg=f'mismatch for values {values}')
            assert_array_almost_equal(_max, _max2, err_msg=f'mismatch for values {values}')
            assert_array_almost_equal(_sum, _sum2, err_msg=f'mismatch for values {values}')

    @unittest.skip("benchmark - run manually")
    def test_custom_stats_benchmark(self):
        # compute_stats is about 10x faster than using scipy + some np methods
        # t1=0.5343782699999999, t2=5.5514434900000005
        v = array('i', [4, 4, 4, 2, 1])

        t1 = timeit(lambda: compute_stats(v), number=10000)
        t2 = timeit(lambda: old_stats(v), number=10000)

        print(f't1={t1}, t2={t2}')

    @unittest.skip("benchmark - run manually")
    def test_median_benchmark(self):
        # statistics.median is about 40x faster than using np.median
        # t1=0.276657643, t2=0.007461202
        v = array('i', [4, 4, 4, 2, 1])

        t1 = timeit(lambda: np.median(v), number=10000)
        t2 = timeit(lambda: statistics.median(v), number=10000)

        print(f't1={t1}, t2={t2}')

    def test_mode(self):
        assert 0 == mode([0])

        assert 0 == mode([0, 0, 1])

        assert 1 == mode([0, 1, 1])

        assert 1 == mode([0, 1, 1, 2, 3, 4, 5])
        assert 1 == mode([0, 1, 1, 2, 3, 4, 5, 5])

        # with equal distribution of values, use first (after sorting)
        assert 0 == mode([5, 4, 3, 2, 1, 0])

        assert 5 == mode([0, 1, 2, 3, 4, 5, 5])