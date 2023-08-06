from setuptools import find_packages, setup

setup(
    name="atro-pyrsync",
    version="0.0.7",
    packages=find_packages(),
    author="Atropos",
    author_email="pypi.rising@atro.xyz",
    description="A simple rsync.wrapper with atro-pylog logging.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/atropos/atro-pylog",
    install_requires=["atro-pylog"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
