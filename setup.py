from setuptools import setup

setup(
    name="journey-cli",
    version="0.1",
    py_modules=["journey"],
    install_requires=["click", "requests"],
    entry_points="""
        [console_scripts]
        journey=journey.cli:cli
    """,
)