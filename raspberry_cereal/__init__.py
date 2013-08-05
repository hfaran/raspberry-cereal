"""raspberry_cereal takes serial input from a shift register
and maps it to any device input you want possible with uinput. Read the
README for details!
"""

import os
import uinput
import time
from ConfigParser import ConfigParser
import argparse
from ast import literal_eval as safe_eval

from raspberry_cereal.sr_74hc165n import gpio_setup, main_loop
from raspberry_cereal.constants import CONFIG_PATH
from raspberry_cereal.validate_cfg import main as validate_config

ARGS = {
    "debug": [
        ("--debug", "-D"),
        "Enables debug mode",  # No debug mode for performance
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
    active_low = safe_eval(config.get('RASPBERRY_CEREAL', 'active_low'))
    # Create device
    events = []
    for key in [config.get('BIT2KEY_MAP', num)
                for num in config.options('BIT2KEY_MAP')
                if config.get('BIT2KEY_MAP', num) != "NONE"]:
        events.append(getattr(uinput, key.upper()))
    device = uinput.Device(events)
    print "[OK] Configuration options type-validated."
    # Setup GPIO
    sr_config = gpio_setup()
    # Set poll time
    poll_time = float(config.get('RASPBERRY_CEREAL', 'poll_time'))

    print ("[OK] If you opened {0} with {1}, you may safely hit Ctrl-C and"
           " {0} will continue to run in the background. Remember to kill"
           " the job when you are done. Polling every {2} ms.".format(
               "raspberry-cereal",
               "'sudo raspberry-cereal &'",
               int(poll_time * 1000)))

    # PERFORMANCE: Moved main_loop so that there are no longer
    # two loops.
    try:
        main_loop(sr_config, active_low, poll_time)
    except KeyboardInterrupt:
        exit("[OK] raspberry-cereal bids you adieu.")
