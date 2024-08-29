import os
import pathlib

import woregnets.dwd as dwd
import woregnets.osm as osm
import woregnets.tiles as tiles
import sys

def create_images(outdir, n=10):
  outPath = pathlib.Path(outdir)
  tileDir = outPath.joinpath("tiles")
  tiles.download_tiles([[64, 70], [39, 46]], 7, tileDir)
  
  worldPath = outPath.joinpath("world_map_xl.png")
  osm.merge_tiles(tileDir, 7).save(worldPath)
  
  dwdPath = outPath.joinpath("dwd/")
  dwd.download_last_n_files_cn_files(dwdPath, n=n)
  
  radar_image_path = outPath.joinpath("radar_images")
  for file in dwdPath.glob("WN*.tar.bz2"):
    dwd.create_rain_image(file, radar_image_path)

if __name__ == '__main__':
  work_dir = sys.argv[1]
  
  pathlib.Path(work_dir).mkdir(parents=True, exist_ok=True)
  
  create_images(work_dir, 10)
