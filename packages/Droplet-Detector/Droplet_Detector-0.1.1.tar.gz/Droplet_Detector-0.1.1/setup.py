from io import open
from setuptools import setup

"""
:authors: Kvas Andrey, Belkova Ksenia, Nekrasova Anna
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2023 kvasik3000
"""

version = '0.1.1'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# with open("requirements.txt", "r") as file:
#     requirements = file.read().splitlines()

setup(
    name='Droplet_Detector',
    version=version,

    author='Kvas Andrey, Belkova Ksenia, Nekrasova Anna',
    author_email='superadrenoline3000@gmail.com',

    description='Telegram bot that draws the outlines of drips on a photo\n'
                '!!! Warning!!! \n'
                'Before running, be sure to create the folders'
                ' "exel", "new_file" and "save_docs" in the '
                'workspace where the python file is located !!!!',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/kvasik3000/Droplet-Detector',

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['Droplet_Detector'],
    install_requires=[
        'numpy==1.24.3',
        'opencv-python==4.7.0.72',
        'openpyxl==3.1.2',
        'pandas==2.0.2',
        'pyTelegramBotAPI==4.11.0',
        'pytest==7.3.2',
        'telebot==0.0.5',
        'matplotlib==3.7.1',
        'pandas-stubs==2.0.2.230605',
        'openpyxl-stubs==0.1.25'
    ],

    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires='==3.9.*',
)
