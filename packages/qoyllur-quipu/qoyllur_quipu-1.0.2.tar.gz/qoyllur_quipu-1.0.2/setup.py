  
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = "1.0.2"
setup(
    name="qoyllur_quipu",
    version=__version__,
    description="q2 Python Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ivan Ramirez",
    author_email="iramirez@tacomacc.edu",
    url="https://github.com/astroChasqui/q2",
    packages=["q2"],
    include_package_data=True,
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib"
    ],
    license="BSD 2-Clause 'Simplified' License",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)
