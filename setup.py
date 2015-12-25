#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    'bravado-core==4.0.0',
    'tornado==4.3',
]

tests_require = [
]

setup(
    name='swagnado',
    version='0.0.1',
    description='Various utilities for integrating Swagger with Tornado',
    author='Justin Crown',
    author_email='justincrown1@gmail.com',
    url='https://github.com/mrname/tornado-swagger-utils',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    license='GNU',
)
