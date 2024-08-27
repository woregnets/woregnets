import tempfile
import unittest.mock

import woregnets.tiles as tiles


class Test(unittest.TestCase):

  @unittest.mock.patch("woregnets.tiles._download")
  def test_download_tiles(self, download_patch):
    download_patch.return_value = bytes("hallo welt", "utf-8")
    with tempfile.TemporaryDirectory(prefix="woregnets") as tmpdir:
      stats = tiles.download_tiles([[40, 41], [44, 45]], 7, tmpdir)
      self.assertEqual(stats, stats | {"downloaded": 1, "skipped": 0})
      stats = tiles.download_tiles([[40, 41], [44, 45]], 7, tmpdir)
      self.assertEqual(stats, stats | {"downloaded": 0, "skipped": 1})
      self.assertEqual(download_patch.call_count, 1)
