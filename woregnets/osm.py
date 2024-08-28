import os

import PIL.Image
import math

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 1 << zoom
  xtile = (lon_deg + 180.0) / 360.0 * n
  ytile = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
  return xtile, ytile


def num2deg(xtile, ytile, zoom):
  n = 1 << zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return lat_deg, lon_deg


def _list_all_tiles(base_dir, zoom_level):
  return [os.path.join(dir, file)
          for [dir, _, files] in os.walk(os.path.join(base_dir, str(zoom_level)))
          if len(files) > 0
          for file in files]


def _parse_tile_name(n):
  (xpath, filename) = os.path.split(n)
  (_, x) = os.path.split(xpath)

  return int(x), int(filename[0:-4]), n

TILES_SIZE = 256

def merge_tiles(base_dir, zoom_level):
  tiles = [_parse_tile_name(n) for n in _list_all_tiles(base_dir, zoom_level)]

  minX = min([x for x, _, _ in tiles])
  maxX = max([x for x, _, _ in tiles])

  minY = min([y for x, y, _ in tiles])
  maxY = max([y for x, y, _ in tiles])

  xTiles = maxX - minX + 1
  yTiles = maxY - minY + 1

  tilesByCoord = dict([[(x, y), filename] for x, y, filename in tiles])

  world_map = PIL.Image.new("RGBA", (xTiles * 256, yTiles * 256))

  for x in range(minX, maxX + 1):
    for y in range(minY, maxY + 1):
      osm_file = tilesByCoord[(x, y)]
      with(PIL.Image.open(osm_file)) as tilePng:
        world_map.paste(tilePng, ((x - minX) * 256, (y - minY) * 256))

  return world_map

# merge_tiles("build/cache", 7).save("build/world_map.png")
