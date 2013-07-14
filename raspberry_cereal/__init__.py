"""raspberry_cereal takes serial input from a shift register
and maps it to any device input you want possible with uinput. Read the
README for details!
"""

import uinput
from ConfigParser import ConfigParser
import time

from raspberry_cereal.custom_device import CustomDevice
from raspberry_cereal.sr_74hc165n import gpio_setup, read_shift_reg
from raspberry_cereal.constants import CONFIG_PATH

def main():
    start = time.time()
    print "Setting up..."
    # Read config file
    config = ConfigParser()
    config.read(CONFIG_PATH)
    POLL_TIME = float(config.get('RASPBERRY_CEREAL', 'poll_time'))
    # Create device
    events = []
    for key in config.options('KEY2BIT_MAP'):
        events.append(eval("uinput.{}".format(key.upper())))
    device = CustomDevice(events)
    # Setup GPIO, create inverse pin/key dict
    sr_config = gpio_setup()
    bit2key_map = {config.get('KEY2BIT_MAP', option):option for option in config.options('KEY2BIT_MAP')}
    print "Finished setup in {} seconds. Polling every {} ms.".format(
                time.time() - start,
                POLL_TIME*1000
        )
    # Poll every POLL_TIME seconds. About 1.6ms per poll for 8 keys
    while(True):
        serial_input = read_shift_reg(sr_config)
        for bit in enumerate(serial_input):
            if bit[1]:
                device.emit_click(
                        eval(
                            "uinput.{}".format(
                                bit2key_map[str(bit[0])].upper()
                        )
                    )
                )
        time.sleep(POLL_TIME)
