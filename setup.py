from setuptools import setup
from raspberry_cereal.constants import CONFIG_PATH
import os
import shutil

# Backup existing config file
if os.path.exists(CONFIG_PATH):
    moved = False
    i = 0
    while not moved:
        if not os.path.exists(CONFIG_PATH+'.bak'+str(i)):
            shutil.move(CONFIG_PATH, CONFIG_PATH+'.bak'+str(i))
            moved = True
        else:
            i += 1

setup(
    name = "raspberry-cereal",
    version = '0.2',
    author = 'Hamza Faran',
    author_email = 'hamza@hfaran.com',
    description = ('A dash of RPi.GPIO and a'
    'sprinkle of python-uinput make for'
    'something that maps serial inputs to'
    'key presses'),
    packages=['raspberry_cereal'],
    install_requires = [
        'RPi.GPIO',
        'python-uinput'
    ],
    data_files = [('/etc/', ['config/raspberry_cereal.cfg'])],
    entry_points = {
        'console_scripts': ['raspberry-cereal = raspberry_cereal:main']
    }
)
