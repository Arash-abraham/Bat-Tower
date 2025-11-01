#!/bin/bash

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

if ! python3 -c "import flask" &> /dev/null; then
    pip install Flask
fi

