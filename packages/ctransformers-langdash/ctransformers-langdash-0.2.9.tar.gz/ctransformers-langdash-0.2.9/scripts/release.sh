#!/bin/bash
rm dist/*
python -m build --sdist
twine upload dist/*