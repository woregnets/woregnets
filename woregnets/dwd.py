import datetime
import os
import re
import tarfile
import urllib.request

import PIL.Image
import bs4
import wradlib

import woregnets.colors as colors
import woregnets.osm as osm

NAME_PATTERN = re.compile("WN(\\d{10}).tar.bz2")

CONTENT_NAME_PATTERN = re.compile("WN(\\d{10})_(\\d\\d\\d).(tar\\.bz2|png)")

INDEX_URL = "https://opendata.dwd.de/weather/radar/composite/wn/"

TIME_FORMAT = "%y%m%d%H%M"


def content_info(file_name):
  return {
    "path": os.path.basename(file_name),
    "name": os.path.basename(file_name)[0:-4],
    "date": datetime.datetime.strptime(CONTENT_NAME_PATTERN.match(file_name)[1], "%y%m%d%H%M")
  }

def _fetch(url):
  with urllib.request.urlopen(url) as resp:
    if resp.status != 200:
      raise Exception("Could not download {}".format(url))
    return resp.read()


def _fetch_xml(url):
  return bs4.BeautifulSoup(_fetch(url), "html.parser")


def _file_name(file_date_time):
  return f"WN{file_date_time.strftime(TIME_FORMAT)}.tar.bz2"


def _file_url(file_date_time):
  return f"{INDEX_URL}{_file_name(file_date_time)}"


def _download_available_cn_file_dates():
  overview = _fetch_xml(INDEX_URL)
  max_date = [x.attrs["href"] for x in overview.body.find_all('a') if NAME_PATTERN.match(x.attrs["href"])]
  return [datetime.datetime.strptime(NAME_PATTERN.match(x)[1], "%y%m%d%H%M") for x in max_date]


def download_last_n_files_cn_files(outdir, n=10):
  os.makedirs(outdir, exist_ok=True)
  all_file_dates = sorted(_download_available_cn_file_dates(), reverse=True)[0:n]

  print(f"Downloading {len(all_file_dates)} files")
  for file_date in all_file_dates:
    content = _fetch(_file_url(file_date))
    target_file = f"{outdir}/{_file_name(file_date)}"
    if not os.path.exists(target_file):
      with open(f"{outdir}/{_file_name(file_date)}", "wb") as f:
        f.write(content)


de1200 = wradlib.georef.get_radolan_grid(nrows=1200, ncols=1100, wgs84=True, mode="edge")

ys = range(39, 46)
xs = range(64, 70)


def create_rain_image(input_file, output_dir, variant="000"):
  rain_img = PIL.Image.new("RGBA", (1536, 1792))
  base_name = os.path.basename(input_file).split(".")[0]
  now_file = f"{base_name}_{variant}"
  print(f"Generating image for file {input_file}: {now_file}")
  with tarfile.open(input_file) as archive:

    radar_data, meta = wradlib.io.read_radolan_composite(archive.extractfile(now_file))

    for dx in range(1200):
      for dy in range(1100):
        tmpx, tmpy = de1200[dx, dy]
        tmpxnext, tmpynext = de1200[dx + 1, dy + 1]
        xtile, ytile = osm.deg2num(tmpy, tmpx, 7)
        xtilenext, ytilenext = osm.deg2num(tmpynext, tmpxnext, 7)
        pixelx, pixely = [(xtile - min(xs)) * 256, (ytile - min(ys)) * 256]
        pixelxnext, pixelynext = [(xtilenext - min(xs)) * 256, (ytilenext - min(ys)) * 256]

        if radar_data[dx, dy] != -9999:
          v = colors.mapval(radar_data[dx, dy])
          if v is not None:
            for x in range(int(pixelx), int(pixelxnext) + 1):
              for y in range(int(pixelynext), int(pixely) + 1):
                if x < rain_img.size[0] and y < rain_img.size[1]:
                  rain_img.putpixel((x, y), PIL.ImageColor.getrgb(v))

  rain_img.save(os.path.join(output_dir, f"{now_file}.png"))
