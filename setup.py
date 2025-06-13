from setuptools import setup, find_packages

setup(
    name="bookman",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click",
        "inquirer",
        "prompt_toolkit",
        "python-dateutil",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "bookman=run:cli",
        ],
    },
    author="alperenozdnc",
    description="A light book management cli",
    license="GPLv3",
)
