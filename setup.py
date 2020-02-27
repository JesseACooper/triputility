from setuptools import setup

setup(
    name="triputility-cli",
    version="0.1",
    py_modules=["triputility"],
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        triputility-cli=triputility.cli:cli
    """,
)