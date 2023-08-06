import inspect
import unittest

import parse_function
from missing_docstring import has_docstring


class TestMissingDocString(unittest.TestCase):

  def test_0(self):
    """
    test with docstring
    :return:
    """
    def function():
      pass
    bool = has_docstring(function)
    self.assertTrue(bool)

    def function2():
      """
      With doc string
      :return:
      """
      pass
    bool = has_docstring(function2)
    self.assertFalse(bool)

  def test_1(self):
    functions = inspect.getmembers(parse_function, inspect.isfunction)
    for function in functions:
        print(f"function {function[0]} {has_docstring(function)}")
