#!/bin/bash

python setup.py install --prefix=~/.local
pushd sample
rm -rf liquipy_changelog.xml
python sample.py
popd