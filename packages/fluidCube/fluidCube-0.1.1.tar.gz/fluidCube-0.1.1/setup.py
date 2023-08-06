
from setuptools import setup

version = '0.1.1'

long_description = 'fluidCube'

setup(
    name = 'fluidCube',
    version = version,

    author = 'Leshin Vladimir, Spektoruk Ilya, Krukovskiy Vasiliy',
    author_email = 'i.spektoruk@g.nsu.ru',

    description = 'fluidCube',
    long_description = long_description,

    url = 'https://github.com/Spektoruk3/PAK',

    packages = ['fluidCube'],
    install_requires = ['numpy', 'pygame', 'sys', 'cv2'],
    )


    