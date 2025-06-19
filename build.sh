#!/usr/bin/env bash






pip install pip==20.1.1
pip install wheel setuptools



# Install Python dependencies

pip install --only-binary :all: greenlet
pip install --only-binary :all: Flask-SQLAlchemy
# Install Python dependencies
pip install -r requirements.txt

