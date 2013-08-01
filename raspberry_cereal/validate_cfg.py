import RPi.GPIO as GPIO
from ConfigParser import ConfigParser
from ast import literal_eval as safe_eval
import uinput
import GPIO

from raspberry_cereal.constants import CONFIG_PATH


def main():
    """Validates config file"""
    config = ConfigParser()
    config.read(CONFIG_PATH)

    # Type validate each entry not in the keymap
    for section in filter(
        lambda s: s != 'BIT2KEY_MAP',
        config.sections()
    ):
        for option in filter(
            lambda o: not o.startswith('type_'),
            config.options(section)
        ):
            if "GPIO_attr" in config.get(section, 'type_' + option):
                assert hasattr(GPIO, config.get(section, option)),
                    ("Config validation failed. GPIO does not have "
                     "attr {}.".format(GPIO, config.get(section, option)))
            assert str(type(safe_eval(config.get(section, option)))) == \
                "<type '{}'>".format(config.get(section, 'type_' + option)),\
                ("Config validation failed. {} expected type was <type '{}'>"
                    ", got {} instead.".format(
                        option,
                        config.get(section, 'type_' + option),
                        str(type(eval(
                            config.get(section, option))))))

    # Validate keymap length
    actual = sorted([int(option) for option in config.options('BIT2KEY_MAP')])
    expected = range(int(config.get(
        'RASPBERRY_CEREAL', 'bus_width')) * int(config.get(
                                                'RASPBERRY_CEREAL', 'shift_registers')))
    assert actual == expected, \
        ("KEY2BIT_MAP does not have items matching specification from"
         " bus_width and shift_registers.\nactual: {}\nexpected: {}".format(
             actual,
             expected))

    # Ensure keys in keymap actually exist
    for key in [
        config.get('BIT2KEY_MAP', key) for key in
            config.options('BIT2KEY_MAP')]:
        assert hasattr(uinput, key), ("The key, {}, is not valid."
                                      .format(key))
