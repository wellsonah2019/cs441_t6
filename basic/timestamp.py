import time
from datetime import datetime

def timestamp():
  now = datetime.now()
  date_time = now.strftime(" [%H:%M:%S] ")

  return date_time
