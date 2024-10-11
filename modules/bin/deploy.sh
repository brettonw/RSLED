#! /usr/bin/env bash

# build, upload, and clean up (because the python build tools don't)
python3 -m build
python3 -m twine upload dist/*
rm -rf build dist setup.cfg
find . -type d -iname *.egg-info -print0 | xargs -0 -I {} rm -rf "{}"
