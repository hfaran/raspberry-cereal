#!/bin/bash

# Make sure the uinput kernel module is enabled
sudo modprobe uinput
# Add uinput to /etc/modules so its loaded on startup
if [ -z $(cat /etc/modules | grep uinput) ]
then
    sudo sh -c 'echo uinput >> /etc/modules'
fi
# Install dependencies
sudo apt-get install python-setuptools python-pip python-dev
# Finally, run the installer
sudo python setup.py install
