# setup.py

from setuptools import setup, find_packages

setup(
    name="Champy",
    version="0.1",
    packages=find_packages(),
    install_requires=["pandas", "plotly"],
    author="Chrysanthos Pepi",
    author_email="cpepis@tamu.edu",
    description="A utility package for ChampSim",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cpepis/Champy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
