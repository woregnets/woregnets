def mapval(val):
  val = (val / 2) - 32.5
  if val < 0:
    return None
  if val < 5:
    return None
    # return "#99ffff7f"
  if val < 10:
    return None
    # return "#33ffff7f"
  if val < 14.5:
    return "#00caca7f"
  if val < 19:
    return "#0099347f"
  if val < 23:
    return "#4dbf1a7f"
  if val < 28:
    return "#99cc007f"
  if val < 32:
    return "#cce6007f"
  if val < 37:
    return "#ffff007f"
  if val < 41:
    return "#ffc4007f"
  if val < 46:
    return "#ff89007f"
  if val < 50:
    return "#ff00007f"
  if val < 55:
    return "#b400007f"
  if val < 60:
    return "#4848ff7f"
  if val < 65:
    return "#0000ca7f"
  if val < 75:
    return "#9900997f"

  return None
