# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='espa_processing',
    package_dir = {'espa_processing': 'processing'},
    version="1.0",
    packages=["espa_processing"],
    include_package_data=False,
    install_requires=["requests"],
    scripts=["scripts/espa-process"],
)
