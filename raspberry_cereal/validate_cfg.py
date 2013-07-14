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
                lambda o: not o.startswith('TYPE_'),
                config.options(section)
            ):
            assert (
                    str(
                        type(
                            eval(
                                config.get(config.get(section, option))))) == \
                                config.get(section, 'TYPE_'+option)),
                    ("Config validation failed. {} expected type was {}"
                     ", got {} instead.".format(
                                option,
                                config.get(section, 'TYPE_'+option)),
                                str(type(eval(
                                    config.get(config.get(section, option)
                                ))))
            )

    assert (
        sorted(
            [config.get('KEY2BIT_MAP', option) for option in \
            config.options('KEY2BIT_MAP')]
        ) == range(config.get(
            'RASPBERRY_CEREAL', 'bus_width')*config.get(
            'RASPBERRY_CEREAL', 'shift_registers')),
        ("KEY2BIT_MAP does not have items matching specification from"
         "bus_width and shift_registers.")
    )
