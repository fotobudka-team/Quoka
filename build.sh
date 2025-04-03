#!/bin/bash

set -e
set -x

PYTHON_VERSION="3.12"
VENV_DIR="venv"

if ! command -v python$PYTHON_VERSION &> /dev/null; then
    echo "Error: Python $PYTHON_VERSION is not installed o your device."
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed on your device."
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo "Error: Docker Compose is not installed on your device."
    exit 1
fi

if [ -d "$VENV_DIR" ]; then
    rm -rf $VENV_DIR
fi

python$PYTHON_VERSION -m venv $VENV_DIR
source $VENV_DIR/bin/activate

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

docker-compose -f docker-compose.dev.yml up --build

deactivate
