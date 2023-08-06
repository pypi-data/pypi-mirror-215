from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nexusdb",
    version="2.1.1",
    author="Pawan kumar",
    author_email="control@vvfin.in",
    include_package_data=True,
    description="A lightweight JSON-based database system for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/E491K8/nexusdb",
    packages=find_packages(),
    py_modules=['nexusdb'],
    install_requires=[
        "uuid"
    ],
    entry_points={
    'console_scripts': [
    'nexus = nexus:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.6',
)
