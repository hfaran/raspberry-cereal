"""This module was written specifically with the 74HC165 in mind, but can
probably be modified to suit any PISO shift register.
"""

import RPi.GPIO as GPIO
from ConfigParser import ConfigParser
from time import sleep
from ast import literal_eval as safe_eval
import uinput

from raspberry_cereal.constants import CONFIG_PATH


def gpio_setup():
    """Performs GPIO setup

    returns:
        Shift register config
    """
    sr_config = {}
    config = ConfigParser()
    config.read(CONFIG_PATH)
    sr_config['ploadpin'] = int(config.get('74HC165N', 'ploadpin'))
    sr_config['datapin'] = int(config.get('74HC165N', 'datapin'))
    sr_config['clockpin'] = int(config.get('74HC165N', 'clockpin'))
    sr_config['triggerpulsewidth'] = float(
        config.get('74HC165N',
                   'triggerpulsewidth')
    )
    sr_config['bus_width'] = int(config.get('RASPBERRY_CEREAL', 'bus_width'))
    sr_config['shift_registers'] = int(config.get(
        'RASPBERRY_CEREAL',
        'shift_registers'
    )
    )
    # PERFORMANCE: Perform this operation here so it only needs to be
    # performed once
    sr_config['full_width'] = sr_config[
        'bus_width'] * sr_config['shift_registers']

    GPIO.setmode(getattr(GPIO, config.get('GPIO', 'setmode')))
    GPIO.setwarnings(safe_eval(config.get('GPIO', 'setwarnings')))
    GPIO.setup(sr_config['ploadpin'], GPIO.OUT)
    GPIO.setup(sr_config['datapin'], GPIO.IN)
    GPIO.setup(sr_config['clockpin'], GPIO.OUT)

    GPIO.output(sr_config['clockpin'], 0)
    GPIO.output(sr_config['ploadpin'], 1)

    return sr_config


def main_loop(sr_config, active_low, poll_time, device, config, args):
    """Reads serial data from shift register"""
    # PERFORMANCE: Move all data from sr_config to locals
    ploadpin = sr_config['ploadpin']
    triggerpulsewidth = sr_config['triggerpulsewidth']
    full_width = sr_config['full_width']
    datapin = sr_config['datapin']
    clockpin = sr_config['clockpin']

    while True:
        GPIO.output(ploadpin, 0)
        sleep(triggerpulsewidth)
        GPIO.output(ploadpin, 1)

        # Uncomment for debug mode, commented out for performance
        # if args.debug:
        #     print "\n"

        # PERFORMANCE: Use xrange instead of range
        for i in xrange(full_width):
            # PERFORMANCE: Removed unnecessary int coersion
            res = GPIO.input(datapin)
            GPIO.output(clockpin, 1)
            sleep(triggerpulsewidth)
            GPIO.output(clockpin, 0)

            # Uncomment for debug mode
            # if args.debug:
            #     print "{}, ".format(res)
            #     continue

            # PERFORMANCE: Key mapping done while reading
            # is happening instead of in separate loop
            key = config.get('BIT2KEY_MAP', str(i)).upper()
            if key != "NONE":
                if res != active_low:
                    device.emit(
                        getattr(uinput, key), 1)
                else:
                    device.emit(
                        getattr(uinput, key), 0)

        sleep(poll_time)
