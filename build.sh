#!/usr/bin/env bash


# Upgrade essential tools
pip install --upgrade pip setuptools wheel

pip install --only-binary :all: greenlet
pip install --only-binary :all: Flask-SQLAlchemy
# Install Python dependencies
pip install -r requirements.txt

