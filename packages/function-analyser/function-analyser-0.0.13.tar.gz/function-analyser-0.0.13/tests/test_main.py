import os
import pathlib
import sys
import unittest
from function_analyser.main import main, get_config


class TestMain(unittest.TestCase):
    def test_0(self):
        main()

    def test_1(self):
        for path in sys.path:
            print(path)

    def test_2(self):
        """
        Search site-packages
        :return:
        """
        sys_path_list = [path for path in sys.path if "site-packages" in path]
        os.chdir(sys_path_list[0])
        main()

    def test_3(self):
        """
        Search Pythin/Lib
        :return:
        """
        sys_path_list = [path for path in sys.path if "Python\Python311\Lib" in path]
        os.chdir(sys_path_list[0])
        main()

    def test_4(self):
        """
        Test for get_config
        :return:
        """
        config_file_name = "test-config.yaml"
        expected_config = {"exclusions": ["./exclusion1", "./exclusion2"]}
        config = get_config(config_file_name)
        self.assertEqual(expected_config, config)
