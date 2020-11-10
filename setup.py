import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mascot-generator",
    version="0.0.1",
    author="Sumit Gogia",
    author_email="sumit.y.gogia@gmail.com",
    description="A simple mascot generator",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/piqueme/mascot-generator",
    packages=setuptools.find_packages(),
    python_requires=">=3.6"
)
