import re
import tempfile
import unittest.mock
from io import BytesIO

import PIL.Image
import PIL.ImageDraw
import woregnets.__main__ as main

TILE_PATTERN = "https://tile.openstreetmap.de/({zoom})/({x})/({y}).png".format(zoom="\\d+", x="\\d+", y="\\d+")

RADAR_PATTERN = "https://opendata.dwd.de/weather/radar/composite/wn/(WN\\d{10}.tar.bz2)"

class MockResponse:

    def __init__(self, bs):
        self.status = 200
        self.bs = bs

    def read(self):
        return self.bs

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass


class ModuleTest(unittest.TestCase):

    @unittest.mock.patch("urllib.request.urlopen")
    def test_main(self, urlopen):
        def open_mock(url):
            if url.startswith("https://tile.openstreetmap.de/"):
                zoom, x, y = re.match(TILE_PATTERN, url).groups()
                bs = BytesIO()
                with PIL.Image.new("RGB", (256, 256), (255, 255, 255)) as tile:
                    draw = PIL.ImageDraw.Draw(tile)
                    draw.text((100, 100), f"({zoom}, {x}, {y})", fill=(0, 0, 0))
                    tile.save(bs, "PNG")
                bs.seek(0)
                return MockResponse(bs.read())
            if url == "https://opendata.dwd.de/weather/radar/composite/wn/":
                with open("testdata/index.html", "r") as index:
                    return MockResponse(index.read())
            if url.startswith("https://opendata.dwd.de/weather/radar/composite/wn/") and url.endswith(".tar.bz2"):
                filename = f"testdata/{re.match(RADAR_PATTERN, url)[1]}"
                with open(filename, "rb") as radar:
                    return MockResponse(radar.read())
            raise Exception(f"Can not handle url {url}")

        urlopen.side_effect = open_mock

        with tempfile.TemporaryDirectory() as tmp:
            main.create_images(tmp, 1)
