"""raspberry_cereal takes serial input from a shift register
and maps it to any device input you want possible with uinput. Read the
README for details!
"""

import os
import uinput
import time
from ConfigParser import ConfigParser
import argparse

from raspberry_cereal.custom_device import CustomDevice
from raspberry_cereal.sr_74hc165n import gpio_setup, read_shift_regs
from raspberry_cereal.constants import CONFIG_PATH, BHZ_PER_CPU_PERCENT
from raspberry_cereal.validate_cfg import main as validate_config

ARGS = {
  "debug": [
    ("--debug", "-D"),
    "Enables debug mode",
    ],
}

def main():
    """Polls shift register for serial data and emit_clicks HIGHs"""
    if os.geteuid() != 0:
        exit("Must be run as root!")
    print "[WAIT] Setting up..."
    # argparse
    parser = argparse.ArgumentParser()
    for arg in ARGS.keys():
        parser.add_argument(*ARGS[arg][0], dest=arg, action='store_true',
            help=ARGS[arg][1])
    args = parser.parse_args()
    # Validate config
    validate_config()
    # Read config file
    config = ConfigParser()
    config.read(CONFIG_PATH)
    #
    ACTIVE_LOW = eval(config.get('RASPBERRY_CEREAL', 'active_low'))
    # Set poll time
    if eval(config.get('RASPBERRY_CEREAL', 'autocalculate_poll_time')):
        poll_time = eval(config.get('RASPBERRY_CEREAL', 'bus_width')) * \
            eval(config.get('RASPBERRY_CEREAL', 'shift_registers')) / \
            BHZ_PER_CPU_PERCENT / eval(config.get('RASPBERRY_CEREAL', \
            'approx_cpu_usage_limit'))
        print "[OK] Poll time calculated: {} ms".format(poll_time*1000)
    else:
        poll_time = float(config.get('RASPBERRY_CEREAL', 'poll_time'))
    # Create device
    events = []
    for key in config.options('KEY2BIT_MAP'):
        events.append(eval("uinput.{}".format(key.upper())))
    device = CustomDevice(events)
    print "[OK] Configuration options type-validated."
    # Setup GPIO, create inverse pin/key dict
    sr_config = gpio_setup()
    bit2key_map = {config.get('KEY2BIT_MAP', option): option
                   for option in config.options('KEY2BIT_MAP')}
    print ("[OK] If you opened {0} with {1}, you may safely hit Ctrl-C and"
           " {0} will continue to run in the background. Remember to kill"
           " the job when you are done. Polling every {2} ms.".format(
               "raspberry-cereal",
               "'sudo raspberry-cereal &'",
               int(poll_time*1000)))

    old_input = [int(ACTIVE_LOW) for i in range(eval(config.get( \
        'RASPBERRY_CEREAL', 'bus_width')) * eval(config.get('RASPBERRY_CEREAL', \
        'shift_registers')))]
    while(True):
        try:
            serial_input = read_shift_regs(sr_config)
            if args.debug:
                print serial_input
            else:
                for bit in enumerate(serial_input):
                   if bit[1] == int(not ACTIVE_LOW) and old_input[bit[0]] == int(ACTIVE_LOW):
                       device.emit_click(
                           eval(
                               "uinput.{}".format(
                                   bit2key_map[str(bit[0])].upper())))
            time.sleep(poll_time)
            old_input = serial_input
        except KeyboardInterrupt:
          exit("[OK] raspberry-cereal bids you adieu.")

