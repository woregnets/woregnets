import os

import chevron

import woregnets.dwd as dwd
import pathlib
import zoneinfo

GERMANY_TZ = zoneinfo.ZoneInfo("Europe/Berlin")

def write_index_html(out_dir, rain_images):
  os.makedirs(out_dir, exist_ok=True)
  mustacheFile = pathlib.Path(__file__).parent.joinpath("index.mustache")
  with open(mustacheFile, 'r') as index_template:
    with open(os.path.join(out_dir, 'index.html'), 'w') as index_html:
      html = chevron.render(index_template, {
        "world_image": "/build/world_map_xl.png",
        "rain_images": rain_images
      })
      index_html.write(html)

def render_html(rain_images_dir, out_dir):
  rain_images = [dwd.content_info(rain_image) for rain_image in os.listdir(rain_images_dir)]

  for rain_image in rain_images:
    rain_image["url"] = "/build/radar_images/" + rain_image["path"]
    rain_image["full_path"] = os.path.join(rain_images_dir, rain_image["path"])
    rain_image["date_string"] = rain_image["date"].astimezone(GERMANY_TZ).strftime("%d.%m.%y %H:%M")
    rain_image["time_string"] = rain_image["date"].astimezone(GERMANY_TZ).strftime("%H:%M")

  rain_images = sorted(rain_images, key=lambda ri: ri["date"])[-10:]

  write_index_html(out_dir, rain_images)

# render_html("build/cache/radar_images", "build/html")
