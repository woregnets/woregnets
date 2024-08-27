import unittest
import importlib


class ModuleTest(unittest.TestCase):
    def test_loading(self):
        importlib.import_module("woregnets")
