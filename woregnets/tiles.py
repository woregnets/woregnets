import os
import urllib.request

def _tile_url(x,y,zoom):
  return f"https://tile.openstreetmap.de/{zoom}/{x}/{y}.png"


def _download(url):
  with urllib.request.urlopen(url) as tile:
    if(tile.status != 200):
      raise Exception(f"Could not fetch tile at url {url}")
    return tile.read()


def download_tiles(area, zoom_level, output_dir):
  downloaded = 0
  skipped = 0

  [[x1, x2], [y1, y2]] = area

  for x in range(x1, x2):
    for y in range(y1, y2):
      target_file = os.path.join(output_dir, f"{zoom_level}/{x}/{y}.png")
      if(not os.path.isfile(target_file)):
        bs = _download(_tile_url(x,y,zoom_level))

        dir = os.path.dirname(target_file)
        os.makedirs(dir, exist_ok=True)
        with open(os.path.join(output_dir, f"{zoom_level}/{x}/{y}.png"), 'wb') as out:
          out.write(bs)
          downloaded = downloaded + 1
      else:
        skipped = skipped + 1

  return {"downloaded": downloaded, "skipped": skipped}

