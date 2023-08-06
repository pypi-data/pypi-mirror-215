import setuptools
from pathlib import Path

setuptools.setup(
    name="terencePDF",
    version=1.0,
    description=Path("README.md").read_text(),
    # this function will look for defined packages in this project, and specific tests and data to be ignored
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
