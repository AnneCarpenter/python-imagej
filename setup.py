# coding=utf-8

from setuptools import setup
import os
import urllib


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
)
