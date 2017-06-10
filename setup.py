#!/usr/bin/env python

from setuptools import setup

version = '0.1.0'

install_requires = [
    'click',
    'requests',
    'terminaltables',
]
setup(
    name='tentacle',
    version=version,
    description='A sample terminal tool for querying detailed information of repositories in Docker Hub',
    long_description=open('README.md').read(),
    author='Fay Cheng',
    author_email='fay.cheng.cn@gmail.com',
    url='https://gihub.com/faycheng/tentacle',
    install_requires=install_requires,
    license='MIT',
    packages=['hub'],
    py_modules=['tentacle'],
    entry_points={
         'console_scripts': ['tentacle=tentacle:cli']},
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
