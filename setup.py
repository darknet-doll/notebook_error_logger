from setuptools import setup, find_packages

setup(
    name="notebook_error_logger",
    version="0.2.0",  # incremented version since functionality changed
    description="Automatic error logging for DS notebooks using pandas & SQLite, with optional Airtable upload.",
    author="darknet-doll",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0.0",
        "pyairtable>=2.1.0"
    ],
    url="https://github.com/darknet-doll/colab_error_logger",
)
