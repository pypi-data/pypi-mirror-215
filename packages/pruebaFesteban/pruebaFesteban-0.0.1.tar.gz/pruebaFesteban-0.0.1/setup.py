from pathlib import Path
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = "0.0.1"
DESCRIPTION = " This package uses and pokemon API to get details about pokemons"
PACKAGE_NAME = "pruebaFesteban"
AUTHOR = "Juan Esteban"
EMAIL = "juanforfreelance@gmail.com"
GITHUB_URL = "https://github.com/TheJuanFreelance/first_Pypi_package/"

setup(
    name=PACKAGE_NAME,
    packages=[PACKAGE_NAME],
    version=VERSION,
    license="MIT",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=GITHUB_URL,
    keywords=[
        "prueba",
    ],
    install_requires=[
        "request",
    ]
)
