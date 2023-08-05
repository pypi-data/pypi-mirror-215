import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "city_planner_project",
    version = "0.0.1",
    author = "Ricardo Simao",
    author_email = "ojogodascontasdevidro@gmail.com",
    description = ("A program helping predict and plan city vehicular flux"),
    license = "GNU",
    keywords = "dynamicalsystems traffic planning",
    url = "http://packages.python.org/city_planner_project",
    packages=['src', 'tests'],
    long_description=read('README.rst'),
    package_dir={'src': 'src'},
    py_modules = ["main", "tools"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "License :: Free For Educational Use",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.8"
    ],
)