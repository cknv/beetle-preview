from setuptools import setup

setup(
    name='beetle_preview',
    author='Esben Sonne',
    author_email='esbensonne+code@gmail.com',
    url='https://github.com/cknv/beetle-preview',
    license='MIT',
    packages=[
        'beetle_preview'
    ],
    install_requires=[
        'watchdog==0.8.1'
    ],
)
