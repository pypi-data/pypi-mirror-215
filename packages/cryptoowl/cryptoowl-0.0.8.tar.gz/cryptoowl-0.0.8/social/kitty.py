import pytz

utc = pytz.utc

def KittyColor(color):
  return color + " kitty in " + utc.zone
