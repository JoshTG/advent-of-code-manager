# Advent of Code Manager

_A pure Python Advent of Code manager_

# At a Glance

This manager provides the following features:

1. Store and manage your input data in one place.
2. Automate the creation and execution of solver scripts for specific days.
3. Handle all aspects of `Advent of Code` in a user-friendly UI.

# Installation

1. Ensure your `python` version is at least `v3.13`.
2. Install [poetry](https://python-poetry.org/).
3. Clone this repository to your local machine.
4. Enter the `advent-of-code-manager` directory via command prompt.
5. Build a virtual environment: `py -m venv .venv`.
6. Connect `poetry` to the virtual environment: `poetry env use .venv/path/to/python`.
7. Download all dependencies: `poetry install`.

# Usage

After the initial setup as outlined in `Installation`, follow these steps:
  
1. Enter the `advent-of-code-manager` directory via command prompt.
2. 


# Acknowledgements

Below are the top-level packages with their licenses.

| Package | Version | Purpose | License |
| ------- | ------- | ------- | ------- |
| [deltalake](https://github.com/delta-io/delta-rs) | >=0.25.5, <1.0.0 | Stores and reads data | Apache Software License (Apache-2.0) |
| [polars](https://github.com/pola-rs/polars) | >=1.30.0, <1.31.0 | Executes DataFrame transformation | MIT License |
| [polta](https://github.com/JoshTG/polta) | >=0.7. 0<1.0.0 | Handles the data storage and transformation | MIT License |
| [pyperclip](https://github.com/asweigart/pyperclip) | >=1.9.0, <1.10.0 | Copies solutions to the user's clipboards | BSD-3-Clause license |
| [shiny](https://github.com/posit-dev/py-shiny) | >=1.4.0,<1.5.0 | Builds the core webapp | MIT License |