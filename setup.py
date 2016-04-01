#!/usr/bin/env python
from setuptools import setup

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='bottle-elastic',
    version='0.2.1',
    url='https://github.com/bsao/bottle-elastic',
    description='Elasticsearch integration for Bottle',
    author='Robson Junior',
    author_email='bsao@icloud.com',
    license='MIT',
    platforms='any',
    py_modules=[
        'bottle_elastic'
    ],
    install_requires=REQUIREMENTS,
    classifiers=[
        'Environment :: Web Environment',
        'Environment :: Plugins',
        'Framework :: Bottle',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
