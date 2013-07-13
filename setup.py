from setuptools import setup

setup(
	name = "raspberry-cereal",
	version = '0.1',
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
	]
)