from setuptools import setup, find_packages

setup(
    name='brew_thermometer',
    version='1.0',
    packages=['tests', 'brew_thermometer'],
    scripts=['bin/brew_thermometerd'],
    install_requires=['paho-mqtt>=1.1'],
    url='',
    license='BSD 3-Clause',
    author='ksletmoe',
    author_email='kyle.sletmoe@gmail.com',
    description='A Python application that runs on a Raspberry Pi and periodically records the temperature from '
                'attached DS18B20 temperature sensor(s), and pushes the values to a web service',
)
