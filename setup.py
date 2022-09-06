import pathlib

from setuptools import setup

here = pathlib.Path(__file__).parent

# Get the long description from the README file
long_description = (here / "README.md").read_text()

dependencies = ["aiohttp==3.8.1", "click==8.1.3", "dacite==1.6.0", "tabulate==0.8.9"]

dev_dependencies = [
    "mypy==0.942",
    "types-requests==2.27.25",
    "types-tabulate==0.8.8",
]


def get_version():
    """Get the version of the app

    Version number is stored as a constant in a file so that
    the argparser can consistently output the same version
    """
    with open(here / "ugent_food/version.py") as fp:
        for line in fp:
            if line.startswith("__version__"):
                return line.split('"')[1]


setup(
    name="ugent-food",
    version=get_version(),
    description="Command-line tool to get the current menu for Ghent University restaurants",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stijndcl/ugent-food",
    license="MIT",
    author="stijndcl",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Dutch",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    keywords="python, food, api, wrapper, zeus, hydra, ugent, ghent, university, resto, restaurants, menu",
    packages=[
        "ugent_food",
        "ugent_food.api",
        "ugent_food.cli",
        "ugent_food.exceptions",
    ],
    python_requires=">=3.9",
    install_requires=dependencies,
    project_urls={
        "Bug Reports": "https://github.com/stijndcl/ugent-food/issues",
        "Source": "https://github.com/stijndcl/ugent-food",
    },
    entry_points={"console_scripts": ["ugent-food = ugent_food:main"]},
)
