import os.path
import unittest
import woregnets.html as html
import tempfile
import pathlib
import bs4


class HtmlTest(unittest.TestCase):

    def test_rendering(self):
        with tempfile.TemporaryDirectory() as tmp:
            index_html = pathlib.Path(tmp, "index.html")
            html.render_html("testdata/html_test", tmp)

            self.assertTrue(index_html.exists())
            bs = bs4.BeautifulSoup(index_html.read_text(encoding='utf-8'), "html.parser")
            self.assertEqual(3, len(bs.find(id="radar_images").find_all("img")))
            self.assertEqual("/images/WN2408220915_000.png", bs.find(id="radar_images").find_all("img")[1]["src"])
            self.assertEqual("/images/WN2408220920_000.png", bs.find(id="radar_images").find_all("img")[2]["src"])
