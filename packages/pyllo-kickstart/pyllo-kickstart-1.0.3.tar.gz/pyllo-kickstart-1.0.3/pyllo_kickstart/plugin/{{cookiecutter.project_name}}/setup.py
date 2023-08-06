# -*- coding: utf-8 -*-
# Copyright © {{cookiecutter.company}}
# Author: {{cookiecutter.author}}

import sys
import os
import os.path as osp
from setuptools import find_packages, setup
#
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


# =============================================================================
# Files added to the package
# =============================================================================
EXTLIST = ['.pyd', '.pot', '.po', '.mo', '.svg', '.png', '.css', '.html', '.js',
           '.ini', '.txt', '.qss', '.ttf', '.json', '.rst', '.bloom',
           '.ico', '.gif', '.mp3', '.ogg', '.sfd', '.bat', '.sh']


install_requires = [
    "pyllo==1.0.0.dev0",
]

if sys.platform == "darwin":
    install_requires += [
        'applaunchservices==0.3.0'
    ]


setup(
    name='{{cookiecutter.project_name}}',
    version='0.0.0.dev0',
    packages=find_packages(),
    package_data={
        '{{cookiecutter.project_name}}': get_package_data('{{cookiecutter.project_name}}', EXTLIST)
    },
    entry_points={
        'pyllo.plugins': [
            f'{{cookiecutter.plugin_class_name|lower}} = {{cookiecutter.project_name}}.plugin:{{cookiecutter.plugin_class_name}}'
        ]
    },
    # include_package_data=True,
    author="{{cookiecutter.author}}",
    author_email="",
    description="{{cookiecutter.plugin_description}}",
    keywords="",
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
