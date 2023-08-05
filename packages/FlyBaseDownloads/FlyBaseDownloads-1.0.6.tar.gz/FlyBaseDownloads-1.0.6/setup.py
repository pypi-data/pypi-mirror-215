#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 17:51:50 2023

@author: javiera.quiroz
"""

from setuptools import setup

setup(
    name='FlyBaseDownloads',
    version='1.0.6',
    license='MIT',
    author='Javiera Quiroz Olave',
    url= 'https://github.com/JavieraQuirozO/FlyBaseDownloads',
    author_email='javiera.quiroz@biomedica.udec.cl',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=open('requirements.txt').readlines(),
    description='Package to download Flybase data in Python, easily and quickly.',
    packages=['FlyBaseDownloads', 'FlyBaseDownloads.classes'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
