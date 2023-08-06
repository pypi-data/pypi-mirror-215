import os
import pathlib
import unittest

import numpy as np
import pandas

from parse_function import FUNCTION_LENGTHS, PARAMETER_COUNT, parse_files
from statistics import get_statistics, filter_series_by_threshold, get_function_lengths_over_threshold, \
    get_parameter_count_over_threshold, apply_thresholds, filter_by_percentile


class TestStatistics(unittest.TestCase):
    def test_0(self):
        """
        Test for get_statistics
        :return:
        """
        series = pandas.Series([1, 2, 3, 4], index=["f1", "f2", "f3", "f4"])
        statistics = get_statistics(series)
        print(statistics)
        self.assertEqual(2.5, statistics["mean"])
        self.assertEqual(2.5, statistics["median"])
        self.assertEqual([1, 2, 3, 4], statistics["mode"])
        self.assertEqual(4, statistics["max"])
        self.assertEqual(1, statistics["min"])

    def test_0a(self):
        """
        Test for get_statistics
        :return:
        """
        series = pandas.Series([1, 2, 3, 4], index=["f1", "f2", "f3", "f4"])
        statistics = get_statistics(series, include_index=True)
        print(statistics)
        self.assertEqual(2.5, statistics["mean"])
        self.assertEqual(2.5, statistics["median"])
        self.assertEqual([1, 2, 3, 4], statistics["mode"])
        self.assertEqual(4, statistics["max"])
        self.assertEqual(1, statistics["min"])

    def test_0b(self):
        """
        Test for series.index.tolist()
        :return:
        """
        series = pandas.Series([1, 2, 3, 4], index=["f1", "f2", "f3", "f4"])
        list = series.index.tolist()
        print(list)

    def test_1(self):
        """
        Tests for filter by threshold
        :return:
        """
        series = pandas.Series([1, 2, 3, 4, 5, 6, 7, 8, 9])
        series = filter_series_by_threshold(series, 5)
        series_list = series.tolist()
        self.assertEqual(4, len(series_list))

    def test_2(self):
        series = pandas.Series([107, 10], index=["function1", "function2"])
        series = get_function_lengths_over_threshold(series)
        series_list = series.tolist()
        self.assertEqual(1, len(series_list))
        self.assertEqual(107, series_list[0])

    def test_3(self):
        series = pandas.Series([3, 7], index=["function1", "function2"])
        series = get_parameter_count_over_threshold(series)
        series_list = series.tolist()
        self.assertEqual(1, len(series_list))
        self.assertEqual(7, series_list[0])

    def test_4(self):
        """
        Tests for apply_thresholds
        :return:
        """
        series = pandas.Series([107, 10], index=["function1", "function2"])
        series.type = FUNCTION_LENGTHS
        series2 = pandas.Series([3, 7], index=["function1", "function2"])
        series2.type = PARAMETER_COUNT
        series_list = [series, series2]
        series_list = apply_thresholds(series_list)
        for series in series_list:
            self.assertTrue(len(series) == 1)
            self.assertTrue(isinstance(series.type, str))

    def test_5a(self):
        series = pandas.Series([1, 2, 3, 4, 5, 6, 7, 8, 9])
        series = series.loc[lambda x: x > np.percentile(x, 95)]
        self.assertEqual(9, series.tolist()[0])

    def test_5(self):
        """
        Test for filter_by_percentile
        :return:
        """
        base_dir = pathlib.Path(__file__).parent
        file_path = os.path.join(base_dir, "..", "src")

        series_list = parse_files(file_path)
        series_list2 = filter_by_percentile(series_list)
        for series in series_list2:
            print(get_statistics(series, include_index=True))

    def test_5(self):
        """
        Test for filter_by_percentile
        80%
        :return:
        """
        base_dir = pathlib.Path(__file__).parent
        file_path = os.path.join(base_dir, "..", "src")

        series_list = parse_files(file_path)
        series_list2 = filter_by_percentile(series_list, percentile=80)
        for series in series_list2:
            print(get_statistics(series, include_index=True))

        worst_offender = series_list2[0].index[-1]
        print(worst_offender)
