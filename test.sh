#!/bin/bash

echo ""
echo "Checking for linting errors"
flake8 --select E,W --max-line-length=140 --ignore E722 pybotcli/
echo "lint errors checked"
echo ""
cd pybotcli/
touch tests/test_manual/__init__.py
echo "checking for unit test"
python -m unittest discover
rm tests/test_manual/__init__.py
echo "unit tests checked"
echo ""