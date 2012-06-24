#!/usr/bin/env python

import vaporize

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='vaporize',
    description='A clean and consistent library for Rackspace Cloud.',
    long_description=open('README.rst').read(),
    author='Michael Lavers',
    author_email='kolanos@gmail.com',
    url='https://github.com/kolanos/vaporize',
    version=vaporize.__version__,
    license='MIT',
    install_requires=open('requirements.txt').readlines(),
    packages=['vaporize']
)
