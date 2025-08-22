# Overview
The purpose of this library is to provide a logger for my other projects. It also
is acting as a learning process for publishing a python module.

# TODO:
- sort out the proper file / function printing

# Messages Package
This is a package that can be included in projects to output messages

Example logging REPO: https://github.com/srtamrakar/python-logger/tree/master

# Installation Process:
```bash
#=======================
# 1. Write the module
#=======================
# Follow this tutorial: https://packaging.python.org/en/latest/tutorials/packaging-projects/

# Required files:
#   setup.py
#   LICENSE
#   README

#=======================
# 2. Build module
#=======================
python3 -m pip install --upgrade build
python3 -m build

#=======================
# 3. Upload module to pypi to be installed
#=======================
# Make sure twin is installed
python3 -m pip install --upgrade twine

# Upload to test server:
python3 -m twine upload --repository testpypi dist/* --verbose

# Upload to real server:
python3 -m twine upload dist/* --verbose

#=======================
# 4. Install the module:
#=======================
# Test Installation
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps phootlogger

# Real installation
python3 -m pip install phootlogger
```


# Repository structure
```bash
run 'tree' at the top of the repo:
.
├── CHANGELOG.md
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
├── setup.py
├── src
│   ├── demo.py
│   └── phootlogger
│       ├── __init__.py
│       └── logger.py
└── tests
    └── phootlogger
        └── test_logger.py
```


### Questions:
    setup.cfg:

    setup.py:
        Instructions to build software. Maybe some configuration options like computing test coverage or unit tests or
        the install prefix.

    pyproject.toml:
        Specifies the project's metadata.
        Used to replace .cfg, but formats everything in TOML. ( Tom's Obvious, Minimal Language: https://en.wikipedia.org/wiki/TOML )
        You can put "Abstract Dependencies" here, but not pinned dependencies. Pinned ones belong in the requirements.txt

    requirements.txt:
        Not the same thing as setup.cfg. Needed for a different reason. This is typically used for deployment with
        version pinned dependencies. The reason is so you don't get the latest and greatest, and only get the version
        you know you have explicitly tested.
