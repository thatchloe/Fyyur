#!/usr/bin/env bash


# Upgrade essential tools
pip install pip==20.1.1
pip install setuptools
pip install python3.11-distutils

# Install Python dependencies

pip install --only-binary :all: greenlet
pip install --only-binary :all: Flask-SQLAlchemy
# Install Python dependencies
pip install -r requirements.txt

