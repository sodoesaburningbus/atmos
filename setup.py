import setuptools

with open("README.txt", "r") as fn:
    long_description = fn.read()

setuptools.setup(
    name="atmos",
    version="1.0.0",
    author="Christopher Phillips of UAH, Huntsville, Alabama",
    author_email="cephillips574@gmail.com",
    description="A python package containing useful functions and constants for atmospheric scientists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sodoesaburningbus/atmos",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU General Public License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
