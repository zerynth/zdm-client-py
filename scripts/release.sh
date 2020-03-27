#!/bin/bash

sudo rm -rf ./dist ./build *.egg-info

echo "##> sdist & wheel"
python setup.py bdist_wheel

echo '##> Uploading sdist to pypi'
twine upload dist/* --skip-existing
