"""Setup file for the Salem package.
   Adapted from the Python Packaging Authority template."""

from setuptools import setup, find_packages  # Always prefer setuptools


DISTNAME = 'dataflow'
LICENSE = 'MIT'
AUTHOR = 'dataflow Developers'
AUTHOR_EMAIL = 'data@glamos.ch'
URL = 'github.com/GLAMOS/dataflow'
CLASSIFIERS = [
        # How mature is this project? Common values are
        # 3 - Alpha  4 - Beta  5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ]

DESCRIPTION = 'data in-/outflow of GLAMOS database'
LONG_DESCRIPTION = """
The dataflow package allows to automatedly read from and write to the GLAMOS 
(Glacier Monitoring Switzerland) database. The package is currently under 
heavy  development and shall provide the necessary code base as well as 
practical examples to retrieve glacier data from the database.

Links
-----
- Source code: https://github.com/GLAMOS/dataflow
"""


req_packages = ['numpy',
                'pandas',
                'matplotlib',
                'psycopg2']


setup(
    # Project info
    name=DISTNAME,
    version=0.1,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    # The project's main homepage.
    url=URL,
    # Author details
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    # License
    license=LICENSE,
    classifiers=CLASSIFIERS,
    # What does your project relate to?
    keywords=['glaciers', 'database', 'climate'],
    # We are a python 3 only shop
    python_requires='>=3.6',
    # Find packages automatically
    packages=find_packages(exclude=['docs']),
    # Install dependencies
    install_requires=req_packages,
    # additional groups of dependencies here (e.g. development dependencies).
    extras_require={},
    # Old
    data_files=[],
    # Executable scripts
    entry_points={},
)