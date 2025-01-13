# setup.py
from setuptools import setup, find_packages

setup(
    name="XTime",
    version="0.3.0",
    packages=find_packages(),
    author="WolfDev",
    author_email="ConexusDevs@email.com",
    description="A custom sleep library for complex proyects.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/XTime",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "xtime=cli:main",
        ],
    },
)