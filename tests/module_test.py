import tempfile
import unittest

import woregnets.__main__ as main


class ModuleTest(unittest.TestCase):

    def test_main(self):
        with tempfile.TemporaryDirectory() as tmp:
            main.create_images(tmp, 2)
