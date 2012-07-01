#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

VERSION = '0.1.6'

setup(
    name='vaporize',
    description='A clean and consistent library for the Rackspace Cloud / OpenStack',
    long_description=open('README.rst').read(),
    author='Michael Lavers',
    author_email='kolanos@gmail.com',
    url='https://github.com/kolanos/vaporize',
    version=VERSION,
    license='MIT',
    install_requires=open('requirements.txt').readlines(),
    data_files=['README.rst', 'requirements.txt', 'LICENSE'],
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
