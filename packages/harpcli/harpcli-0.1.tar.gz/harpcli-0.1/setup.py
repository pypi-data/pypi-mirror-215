from setuptools import setup

setup(
    name="harpcli",  # change this to whatever you want to name your CLI tool
    version="0.1",
    description="CLI for the harp API",
    py_modules=["main"],  # this should be the name of your python script file
    author="harpdevs",
    install_requires=[
        "typer",
        "requests",
    ],
    entry_points="""
        [console_scripts]
        harp=main:app
    """,
    zip_safe=False,
    license="MIT",
)
