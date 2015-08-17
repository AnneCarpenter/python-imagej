# coding=utf-8

import sys
from setuptools import setup
import os
import urllib
from setuptools.command.test import test


class PyTest(test):
    user_options = [
        ('pytest-args=', 'a', "Arguments to pass to py.test"),
    ]

    def initialize_options(self):
        test.initialize_options(self)

        self.pytest_args = []

    def finalize_options(self):
        test.finalize_options(self)

        self.test_args = []

        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)

        sys.exit(errno)


def retrieve_prokaryote(version='1.0.0'):
    url = 'https://github.com/CellProfiler/prokaryote/releases/download/{0}/prokaryote-{0}.jar'.format(version)

    filename = './prokaryote-{0}.jar'.format(version)

    if not os.path.isfile(filename):
        urllib.urlretrieve(url, filename)

    return filename


setup(
    name='imagej',
    version='0.0.1',
    description='…',
    long_description='…',
    url='https://github.com/pypa/sampleproject',
    author='The Python Packaging Authority',
    author_email='pypa-dev@googlegroups.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='sample setuptools development',
    packages=[
        'imagej',
    ],
    install_requires=[
        'bioformats',
        'javabridge',
        'numpy',
        'pytest',
    ],
    # package_data={
    #     'prokaryote': [
    #         retrieve_prokaryote()
    #     ],
    # },
    extras_require={
        'test': [
            'coverage'
        ],
    },
    tests_require=[
        'pytest',
    ],
    cmdclass={
        'test': PyTest,
    },
)
