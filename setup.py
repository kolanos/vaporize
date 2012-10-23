#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

VERSION = '0.2.3'

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name='vaporize',
    description='A clean and consistent library for the Rackspace Cloud / OpenStack',
    long_description=read('README.rst'),
    author='Michael Lavers',
    author_email='kolanos@gmail.com',
    url='https://github.com/kolanos/vaporize',
    version=VERSION,
    license='MIT',
    install_requires=['python-dateutil', 'requests'],
    tests_require=['nose'],
    test_suite='nose.collector',
    packages=['vaporize'],
    keywords="rackspace openstack cloudservers cloudloadblancers clouddns",
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
