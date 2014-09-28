from setuptools import setup

setup(
    name='beetle_preview',
    version='0.1.0'
    author='Esben Sonne',
    author_email='esbensonne+code@gmail.com',
    description='Local test server plugin for Beetle',
    url='https://github.com/cknv/beetle-preview',
    license='MIT',
    packages=[
        'beetle_preview'
    ],
    install_requires=[
        'watchdog'
    ],
)
