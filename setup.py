#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '0.1.9'

try:
    readme = open('README.rst').read()
except IOError:
    readme = ''

setup(
    name='vaporize',
    description='A clean and consistent library for the Rackspace Cloud / OpenStack',
    long_description=readme,
    author='Michael Lavers',
    author_email='kolanos@gmail.com',
    url='https://github.com/kolanos/vaporize',
    version=VERSION,
    license='MIT',
    install_requires=['python-dateutil', 'requests'],
    #data_files=['README.rst', 'requirements.txt', 'LICENSE'],
    packages=['vaporize'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing',
        'Topic :: Utilities',
    ],
)
