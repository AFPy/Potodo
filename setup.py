#!/usr/bin/env python3

import setuptools

import potodo

with open("README.md") as readme:
    long_description = readme.read()

setuptools.setup(
    name="potodo",
    version=potodo.__version__,
    description="Will list all .po files that are to be transated",
    long_description=long_description,
    long_description_content_type="text/markdown",  # This is important!
    author="Jules Lasne",
    author_email="jules.lasne@gmail.com",
    url="https://github.com/seluj78/potodo",
    packages=["potodo"],
    package_dir={"potodo": "potodo"},
    entry_points={"console_scripts": ["potodo=potodo.potodo:main"]},
    include_package_data=True,
    install_requires=["polib", "requests"],
    license="MIT license",
    zip_safe=False,
    keywords="potodo",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.6",
)
