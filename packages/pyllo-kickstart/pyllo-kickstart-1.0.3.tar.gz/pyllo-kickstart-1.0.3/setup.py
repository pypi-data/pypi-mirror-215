# -*- coding: utf-8 -*-
# Copyright © Connet Information Technology Company, Shanghai.

from setuptools import find_packages, setup
import sys
import os
import os.path as osp

# =============================================================================
# Minimal Python version sanity check
# Taken from the notebook setup.py -- Modified BSD License
# =============================================================================
v = sys.version_info
if v[0] >= 3 and v[:2] < (3, 6):
    error = "ERROR: Pyllo requires Python version 3.6 and above."
    print(error, file=sys.stderr)
    sys.exit(1)


# =============================================================================
# Constants
# =============================================================================
NAME = 'pyllo-kickstart'
LIBNAME = 'pyllo_kickstart'
HERE = os.path.abspath(os.path.dirname(__file__))

# =============================================================================
# Auxiliary functions
# =============================================================================
def get_package_data(name, extlist):
    """
    Return data files for package *name* with extensions in *extlist*.
    """
    flist = []
    # Workaround to replace os.path.relpath (not available until Python 2.6):
    offset = len(name)+len(os.pathsep)
    for dirpath, _dirnames, filenames in os.walk(name):
        if 'tests' not in dirpath:
            for fname in filenames:
                if (not fname.startswith('.') and
                        osp.splitext(fname)[1] in extlist):
                    flist.append(osp.join(dirpath, fname)[offset:])
    return flist

def get_description():
    """Get long description."""
    with open(os.path.join(HERE, 'README.md'), 'r') as f:
        data = f.read()
    return data



# =============================================================================
# Files added to the package
# =============================================================================
EXTLIST = ['.json', '.py']


install_requires = [
    "pyllo>=1.0.0.dev0",
    "rich==13.3.5",
    "cookiecutter==2.1.1"
]

if sys.platform == "darwin":
    install_requires += [
        'applaunchservices==0.3.0'
    ]


setup(
    name=NAME,
    version="1.0.3",
    packages=find_packages(),
    package_data={LIBNAME: get_package_data(LIBNAME, EXTLIST)},
    entry_points={
        'console_scripts': [
            'pyllo-kickstart=pyllo_kickstart.main:main',
        ]
    },
    author="Shanghai Connet Information Technology Company Ltd.",
    author_email="tech_support@shconnet.com.cn",
    description="Pyllo plugin generator",
    long_description=get_description(),
    long_description_content_type='text/markdown',
    keywords="pyllo plugin template generator",
    url="",   # project home page
    project_urls={
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Interpreters",
    ],
    install_requires=install_requires,
)
