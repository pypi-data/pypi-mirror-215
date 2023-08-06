# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup

with open('requirements.txt') as f:
    required_raw = f.read().strip().splitlines()
    REQUIRED = [line.strip() for line in required_raw if not line.startswith('#')]

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "scrapy_manipulate_request", "__version__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()


setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    description=about["__description__"],
    license=about["__license__"],
    url=about["__url__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email=about["__email__"],
    python_requires=">=3.7.0",
    packages=find_packages(exclude=('test', 'example')),
    include_package_data=True,
    package_data={
        '': ['*'],
    },
    install_requires=REQUIRED,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
    ],
)