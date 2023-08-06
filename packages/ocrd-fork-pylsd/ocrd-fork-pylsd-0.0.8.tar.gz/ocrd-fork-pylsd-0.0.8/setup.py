#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, Extension

clib = Extension('pylsd.lib',
                 sources=['source/src/lsd.cpp'],
                 include_dirs=['source/include'],
                 depends=['source/include/lsd.h'],
                 language="c++")

setup(
    name='ocrd-fork-pylsd',
    version='0.0.8',
    description='pylsd is the python bindings for LSD - Line Segment Detector',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Gefu Tang',
    author_email='tanggefu@gmail.com',
    maintainer='kba',
    license='AGPL',
    keywords=["LSD", 'line segmentation'],
    url='https://github.com/OCR-D/pylsd',
    packages=['pylsd', 'pylsd.bindings'],
    install_requires=['numpy'],
    ext_modules=[clib],
)
