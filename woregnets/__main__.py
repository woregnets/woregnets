import pathlib

import woregnets.dwd as dwd
import woregnets.osm as osm
import woregnets.tiles as tiles
import woregnets.html as html
import sys

def create_images(outdir, n=10):
  outPath = pathlib.Path(outdir)
  outPath.mkdir(parents=True, exist_ok=True)
  tileDir = outPath.joinpath("tiles")
  tiles.download_tiles([[64, 70], [39, 46]], 7, tileDir)
  
  worldPath = outPath.joinpath("world_map_xl.png")
  osm.merge_tiles(tileDir, 7).save(worldPath)
  
  dwdPath = outPath.joinpath("dwd/")
  dwd.download_last_n_files_cn_files(dwdPath, n=n)
  
  radar_image_path = outPath.joinpath("radar_images")
  for file in sorted(dwdPath.glob("WN*.tar.bz2"))[-n:]:
    dwd.create_rain_image(file, radar_image_path)
      
  htmlPath = outPath.joinpath("html")
  html.render_html(radar_image_path, htmlPath)

if __name__ == '__main__':
  work_dir = sys.argv[1]
  print(work_dir)

  create_images("build", 10)