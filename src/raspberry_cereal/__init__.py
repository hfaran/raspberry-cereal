import uinput
from ConfigParser import ConfigParser

from raspberry_cereal.custom_device import CustomDevice
from raspberry_cereal.sr_74hc165n import gpio_setup, \
    read_shift_reg
from raspberry_cereal.constants import CONFIG_PATH

def main():
    config = ConfigParser()
    config.read(CONFIG_PATH)

    events = []
    for key in config.options('KEY2BIT_MAP'):
        events.append(eval("uinput.{}".format(key.upper())))

    sr_config = gpio_setup()
    bit2key_map = {config.get('KEY2BIT_MAP', option):option for option in config.options('KEY2BIT_MAP')}

    while(True):
        serial_input = read_shift_reg(sr_config)
        for bit in enumerate(serial_input):
            if bit[1]:
                device.emit_click(eval("uinput.{}".format(bit2key_map[int(bit[0])])))
