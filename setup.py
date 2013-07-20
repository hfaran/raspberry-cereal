from setuptools import setup
from raspberry_cereal.constants import CONFIG_PATH, CONFIG_DIR
import os
import shutil

response = None
# Make sure path exists
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)
# Backup existing config file
if os.path.exists(CONFIG_PATH):
    print ("[WARNING] Existing config file found. Would you like to "
           "keep the existing file, or replace it with a new one? "
           "The existing file may not be backwards-compatible.")
    while response != "keep" and response != "replace":
        response = raw_input("keep or replace?")

if response == "replace":
    moved = False
    i = 0
    while not moved:
        if not os.path.exists(CONFIG_PATH+'.bak'+str(i)):
            print ("[WARNING] Existing config file will be backed up "
                   "as {} and replaced with the new file from the "
                   "repository.".format(
                        CONFIG_PATH+'.bak'+str(i)
                    ))
            if raw_input("continue? (y/n)") != "y":
                exit("Quitting; no changes made.")
            shutil.move(CONFIG_PATH, CONFIG_PATH+'.bak'+str(i))
            moved = True
        else:
            i += 1

setup(
    name="raspberry-cereal",
    version='1.0',
    author='Hamza Faran',
    author_email='hamza@hfaran.com',
    description=('Serial GPIO-to-USB utility for Raspberry Pi'),
    packages=['raspberry_cereal'],
    install_requires = [
        'RPi.GPIO',
        'python-uinput'
    ],
    data_files=[(CONFIG_DIR, ['config/raspberry_cereal.cfg'])],
    entry_points={
        'console_scripts': ['raspberry-cereal = raspberry_cereal:main']
    }
)
