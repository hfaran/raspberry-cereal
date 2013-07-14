import uinput
from ConfigParser import ConfigParser

from raspberry_cereal.custom_device import CustomDevice
#from raspberry_cereal.sr_74hc165n import gpio_setup, \
#    iread, read_shift_reg
from raspberry_cereal.constants import CONFIG_PATH

def main():
    config = ConfigParser()
    config.read(CONFIG_PATH)

    events = []
    for key in config.options('KEY2BIT_MAP'):
        events.update(eval("uinput.{}".format(key.upper())))
