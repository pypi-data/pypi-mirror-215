import os
import pathlib
import unittest
import pandas
from pandas import Series

from function_analyser.parse_function import parse_file, parse_files, FUNCTION_LENGTHS, PARAMETER_COUNT, create_series


class TestParseFunctions(unittest.TestCase):

    def test_0(self):
        """
        Test for custom series attribute
        :return:
        """
        d = {"function1": 10, "function2": 24, "file": "filename"}
        series = pandas.Series(data=d, index=["function1", "function2"])
        # add custom attribute to a series ...
        series.filename = "filename"
        self.assertEqual(2, len(series))
        self.assertTrue(isinstance(series.filename, str))

    def test_3(self):
        """
        Test for create_series
        :return:
        """
        data = [1, 2, 3, 4]
        index = ["f1", "f2", "f3", "f4"]
        series = create_series(data, index, "type")
        self.assertTrue(isinstance(series, Series))
        self.assertTrue(["f1", "f2", "f3", "f4"], series.index.tolist())

    def test_4(self):
        """
        Tests for parse_file
        No thresholds
        :return:
        """
        base_dir = pathlib.Path(__file__).parent
        file = os.path.join(base_dir, "..", "src", "function_analyser", "parse_function.py")
        with open(file) as file:
            series_list = parse_file(file)
            self.assertEqual(6, len(series_list[0]))
            self.assertTrue(isinstance(series_list[0].filename, str))

    def test_5(self):
        """
        Test for parse_file
        :return:
        """
        base_dir = pathlib.Path(__file__).parent
        file = os.path.join(base_dir, "test_parse_function.py")
        with open(file) as file:
            series_list = parse_file(file)
            self.assertEqual(2, len(series_list))

    def test_6(self):
        """
        Test for parse_files

        :return:
        """
        base_dir = pathlib.Path(__file__).parent
        series_list = parse_files(base_dir)
        self.assertEqual(2, len(series_list))
        self.assertEqual(FUNCTION_LENGTHS, series_list[0].type)
        self.assertTrue(len(series_list[0]) > 0)
        self.assertEqual(PARAMETER_COUNT, series_list[1].type)
        self.assertTrue(len(series_list[1]) > 0)

    def test_7(self):
        """
        Test for parse_files

        No source files
        :return:
        """
        base_dir = pathlib.Path(__file__).parent.parent
        series_list = parse_files(base_dir)
        self.assertEqual(0, len(series_list))


if __name__ == '__main__':
    unittest.main()
