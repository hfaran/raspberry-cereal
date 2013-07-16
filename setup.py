from setuptools import setup
from raspberry_cereal.constants import CONFIG_PATH, CONFIG_DIR
import os
import shutil

# Make sure path exists
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_PATH)
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
    name="raspberry-cereal",
    version='0.3',
    author='Hamza Faran',
    author_email='hamza@hfaran.com',
    description=('Serial GPIO-to-USB utility for Raspberry Pi'),
    packages=['raspberry_cereal'],
    install_requires = [
        'RPi.GPIO',
        'python-uinput'
    ],
    data_files=[('/etc/raspberry-cereal/', ['config/raspberry_cereal.cfg'])],
    entry_points={
        'console_scripts': ['raspberry-cereal = raspberry_cereal:main']
    }
)
