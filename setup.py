from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")


def read_requirements() -> list[str]:
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="ugent-food",
    version="0.1.0",
    description="Utility package to validate values based on type annotations",
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
    packages=find_packages(include=["type_validators"]),
    python_requires=">=3.9",
    install_requires=read_requirements(),
    project_urls={
        "Bug Reports": "https://github.com/stijndcl/ugent-food/issues",
        "Source": "https://github.com/stijndcl/ugent-food",
    },
    entry_points={
        "console_scripts": [
            "ugent-food = ugent_food:main"
        ]
    }
)
