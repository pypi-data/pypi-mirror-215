#!/usr/bin/env python
import sys
from setuptools import find_namespace_packages, setup, find_packages

package_name = "spt_factory"
package_version = "0.0.28"
description = """SPT resource manager"""


if sys.version_info < (3, 7):
    print("Error: spt-factory does not support this version of Python.")
    print("Please upgrade to Python 3.7 or higher.")
    sys.exit(1)


setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=description,
    author='Mark Poroshin',
    author_email='mporoshin@smartpredictiontech.ru',
    packages=find_namespace_packages(include=[
        'spt_factory',
        'spt_factory.*'
    ]),
    # url="https://gitlab.com/dv_group/dv_elt_lib",
    include_package_data=True,
    install_requires=[
        "psycopg2-binary~=2.9.3",
        "pymongo~=4.1.1",
        "boto3~=1.24.45",
        "prometheus_client==0.15.0",
        "python-logging-loki==0.3.1",
        "clickhouse-driver==0.2.6",
        "pandas"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
      ],
)
