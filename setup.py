import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NotAOrm",
    python_requires='>=3.6',
    version="0.1.1",
    author="ludel",
    author_email="ludel47@gmail.com",
    description="A sample python library for managing a SQLite database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ludel/NotAOrm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
