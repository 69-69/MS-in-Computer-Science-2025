#!/bin/bash

# Create a virtual environment
echo 'creating virtual environment'
python3 -m venv venv

# Activate the virtual environment
echo 'activating virtual environment'
source venv/bin/activate

# Install dependencies
echo 'installing requirements'
pip install -r requirements.txt

# Start the Flask app
echo 'starting server'
python app.py