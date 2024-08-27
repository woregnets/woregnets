import os
import tempfile
import unittest

import PIL.Image

import woregnets.osm as osm


class OsmTest(unittest.TestCase):
  def setUp(self):
    self._dir = tempfile.TemporaryDirectory(prefix="osm")
    os.makedirs(os.path.join(self._dir.name, "7/0"), exist_ok=True)
    os.makedirs(os.path.join(self._dir.name, "7/1"), exist_ok=True)
    PIL.Image.new("RGBA", (256, 256), (255, 0, 0, 255)).save(os.path.join(self._dir.name, "7/0/0.png"))
    PIL.Image.new("RGBA", (256, 256), (0, 255, 0, 255)).save(os.path.join(self._dir.name, "7/0/1.png"))
    PIL.Image.new("RGBA", (256, 256), (0, 0, 255, 255)).save(os.path.join(self._dir.name, "7/1/0.png"))
    PIL.Image.new("RGBA", (256, 256), (0, 0, 0, 255)).save(os.path.join(self._dir.name, "7/1/1.png"))

  def tearDown(self):
    self._dir.cleanup()

  def test_tile_merging(self):
    merged = osm.merge_tiles(self._dir.name, 7)
    self.assertEqual((255, 0, 0, 255), merged.getpixel((100, 100)))
    self.assertEqual((0, 0, 255, 255), merged.getpixel((300, 100)))
    self.assertEqual((0, 255, 0, 255), merged.getpixel((100, 300)))
    self.assertEqual((0, 0, 0, 255), merged.getpixel((300, 300)))

    self.assertEqual((256 * 2, 256 * 2), merged.size)
