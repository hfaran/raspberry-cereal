import time
import uinput

class CustomDevice(uinput.Device):
  """Extended version of python-uinput v0.9 Device class"""
  def __init__(self, *args, **kwargs):
    super(CustomDevice, self).__init__(*args, **kwargs)
    time.sleep(1)
  def emit_click(self, key):
    """Emits a press and a depress"""
    self.emit(key, 1)
    self.emit(key, 0)
