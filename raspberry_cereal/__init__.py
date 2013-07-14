"""raspberry_cereal takes serial input from a shift register
and maps it to any device input you want possible with uinput. Read the
README for details!
"""

import uinput
import time
from ConfigParser import ConfigParser

from raspberry_cereal.custom_device import CustomDevice
from raspberry_cereal.sr_74hc165n import gpio_setup, read_shift_regs
from raspberry_cereal.constants import CONFIG_PATH

def main():
    """Polls shift register for serial data and emit_clicks HIGHs"""
    print "[WAIT] Setting up..."
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
    print ("[OK] If you opened {0} with {1}, you may safely hit Ctrl-C and"
           " {0} will continue to run in the background. Remember to kill"
           " the job when you are done. Polling every {2} ms.".format(
                "raspberry-cereal",
                "'sudo raspberry-cereal &",
                int(POLL_TIME*1000)
            )
        )
    # Poll every POLL_TIME seconds. About 1.6ms per poll for 8 keys
    while(True):
        serial_input = read_shift_regs(sr_config)
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
