"""raspberry_cereal takes serial input from a shift register
and maps it to any device input you want possible with uinput. Read the
README for details!
"""

import os
import uinput
import time
from ConfigParser import ConfigParser
import argparse

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
    # Create device
    events = []
    for key in [config.get('BIT2KEY_MAP', num) \
            for num in config.options('BIT2KEY_MAP') \
            if config.get('BIT2KEY_MAP', num) != "NONE"]:
        events.append(eval("uinput.{}".format(key.upper())))
    device = uinput.Device(events)
    print "[OK] Configuration options type-validated."
    # Setup GPIO
    sr_config = gpio_setup()
    # Set poll time
    if eval(config.get('RASPBERRY_CEREAL', 'autocalculate_poll_time')):
        poll_time = test(sr_config, device, 10000)
        print "[OK] Poll time calculated: {} ms".format(poll_time*1000)
    else:
        poll_time = float(config.get('RASPBERRY_CEREAL', 'poll_time'))

    print ("[OK] If you opened {0} with {1}, you may safely hit Ctrl-C and"
           " {0} will continue to run in the background. Remember to kill"
           " the job when you are done. Polling every {2} ms.".format(
               "raspberry-cereal",
               "'sudo raspberry-cereal &'",
               int(poll_time*1000)))

    while(True):
        try:
            serial_input = read_shift_regs(sr_config)
            if args.debug:
                print serial_input
            else:
                emit_key(serial_input, config, device)
            time.sleep(poll_time)
        except KeyboardInterrupt:
          exit("[OK] raspberry-cereal bids you adieu.")

def test(sr_config, device, RUNS):
    """Times RUNS runs and returns poll_time based on the specified"""
    start = time.time()
    for i in range(RUNS):
        serial_input = read_shift_regs(sr_config)
        device.emit(uinput.KEY_UNKNOWN, 0)
    return (float(RUNS)/(time.time() - start))*(eval(config.get('RASPBERRY_CEREAL', 'approx_cpu_usage_limit'))/100.0)

def emit_key(serial_input, config, device):
    for bit in enumerate(serial_input):
        key = config.get('BIT2KEY_MAP', str(bit[0])).upper()
        if key != "NONE":
            if bit[1] == int(not ACTIVE_LOW):
                device.emit(
                    eval("uinput.{}".format(key)), 1)
            else:
                device.emit(
                    eval("uinput.{}".format(key)), 0)
