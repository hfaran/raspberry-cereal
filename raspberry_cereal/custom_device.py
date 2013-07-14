import uinput

class CustomDevice(uinput.Device):
  """Extended version of python-uinput v0.9 Device class"""
  def emit_click(self, key):
    """Emits a press and a depress"""
    self.emit(key, 1)
    self.emit(key, 0)
