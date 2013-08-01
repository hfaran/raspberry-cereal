"""This module was written specifically with the 74HC165 in mind, but can
probably be modified to suit any PISO shift register.
"""

import RPi.GPIO as GPIO
from ConfigParser import ConfigParser
from time import sleep
from ast import literal_eval as safe_eval

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

    GPIO.setmode(getattr(GPIO, config.get('GPIO', 'setmode')))
    GPIO.setwarnings(safe_eval(config.get('GPIO', 'setwarnings')))
    GPIO.setup(sr_config['ploadpin'], GPIO.OUT)
    GPIO.setup(sr_config['datapin'], GPIO.IN)
    GPIO.setup(sr_config['clockpin'], GPIO.OUT)

    GPIO.output(sr_config['clockpin'], 0)
    GPIO.output(sr_config['ploadpin'], 1)

    return sr_config


def read_shift_regs(sr_config):
    """Reads serial data from shift register"""
    bit_val = 0
    serial_input = []

    GPIO.output(sr_config['ploadpin'], 0)
    sleep(sr_config['triggerpulsewidth'])
    GPIO.output(sr_config['ploadpin'], 1)

    for i in range(sr_config['bus_width'] * sr_config['shift_registers']):
        serial_input.append(int(GPIO.input(sr_config['datapin'])))
        GPIO.output(sr_config['clockpin'], 1)
        sleep(sr_config['triggerpulsewidth'])
        GPIO.output(sr_config['clockpin'], 0)

    return serial_input
