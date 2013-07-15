import RPi.GPIO as GPIO
from ConfigParser import ConfigParser
from raspberry_cereal.constants import CONFIG_PATH


def main():
    """Validates config file"""
    config = ConfigParser()
    config.read(CONFIG_PATH)

    for section in filter(
        lambda s: s != 'KEY2BIT_MAP',
        config.sections()
    ):
        for option in filter(
            lambda o: not o.startswith('type_'),
            config.options(section)
        ):
            assert str(type(eval(config.get(section, option)))) == \
                "<type '{}'>".format(config.get(section, 'type_'+option)),\
                ("Config validation failed. {} expected type was <type '{}'>"
                    ", got {} instead.".format(
                        option,
                        config.get(section, 'type_'+option),
                        str(type(eval(
                            config.get(section, option))))))

    assert sorted(
        [int(config.get('KEY2BIT_MAP', option)) for option in
            config.options('KEY2BIT_MAP')]
    ) == range(int(config.get(
        'RASPBERRY_CEREAL', 'bus_width'))*int(config.get(
        'RASPBERRY_CEREAL', 'shift_registers'))), \
        ("KEY2BIT_MAP does not have items matching specification from"
         " bus_width and shift_registers.")
