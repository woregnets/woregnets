import os.path
from unittest import TestCase
import wradlib.georef as georef
import woregnets.dwd as dwd
import tempfile
import PIL.Image


class DepTest(TestCase):

    def setUp(self):
        self._grid = georef.get_radolan_grid(nrows=1200, ncols=1100, wgs84=True, mode="edge",
                                             proj=georef.create_osr("dwd-radolan-wgs84-de1200"))

    def test_coord_system_size(self):
        self.assertEqual(1201, len(self._grid))
        for i in self._grid:
            self.assertEqual(1101, len(i))
            
class RainImageTest(TestCase):

    def test_create_rain_image(self):
        with tempfile.TemporaryDirectory() as dir:
            dwd.create_rain_image("testdata/WN2408220915.tar.bz2", dir)
            output_file = os.path.join(dir, "WN2408220915_000.png")

            self.assertTrue(os.path.exists(output_file))
            
            with PIL.Image.open(output_file) as target_image:
                self.assertEqual((1536, 1792), target_image.size)
