import setuptools
import setuptools.command.test
import sys

class Test(setuptools.command.test.test):
    user_options = [
        ("pytest-args=", "a", "Arguments to pass to py.test")
    ]

    def initialize_options(self):
        setuptools.command.test.test.initialize_options(self)

        self.pytest_args = []

    def finalize_options(self):
        setuptools.command.test.test.finalize_options(self)

        self.test_args = []

        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)

        sys.exit(errno)


setuptools.setup(
    author="Allen Goodman",
    author_email="agoodman@broadinstitute.org",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering",
    ],
    cmdclass={
        "test": Test,
    },
    description="",
    install_requires=[
        'javabridge',
        'numpy',
        'python-bioformats',
    ],
    keywords="",
    license="BSD",
    long_description="",
    name="centrosome",
    packages=[
        "imagej"
    ],
    tests_require=[
        "pytest",
    ],
    url="https://github.com/CellProfiler/python-imagej",
    version="1.0.0",
)
