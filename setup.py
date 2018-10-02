import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NotAOrm",
    version="0.0.1",
    author="ludel",
    author_email="ludel47@gmail.com",
    description="Python methods for managing a SQLite database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ludel/NotAOrm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "The Unlicense",
        "Operating System :: OS Independent",
    ],
)
