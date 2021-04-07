import setuptools

with open("README.txt", "r") as fn:
    long_description = fn.read()

setuptools.setup(
    name="atmos",
    version="1.1.0",
    author="Christopher Phillips of UAH, Huntsville, Alabama",
    author_email="cephillips574@gmail.com",
    description="A python package containing useful functions and constants for atmospheric scientists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sodoesaburningbus/atmos",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU General Public License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires='>=3.0',
)
