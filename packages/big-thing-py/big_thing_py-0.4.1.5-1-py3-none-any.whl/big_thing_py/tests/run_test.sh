#!/bin/bash

VENV_NAME="pytest_env"
PYTHON_VERSION="3.10.6"

# Check if virtualenv module is installed
if ! command -v virtualenv &> /dev/null; then
  echo "virtualenv module not found. Installing..."
  pip install virtualenv
fi

# Check if virtual environment exists
if [ -d "$VENV_NAME" ]; then
  echo "Virtual environment $VENV_NAME exists"
else
  echo "Creating virtual environment $VENV_NAME"
  virtualenv -p python$PYTHON_VERSION $VENV_NAME
fi

# Activate virtual environment
source $VENV_NAME/bin/activate

# Install dependencies
pip install -r ../../requirements.txt

# Run pytest
pytest "$@"

# Deactivate virtual environment
deactivate
