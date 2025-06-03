#!/bin/bash
cd ../backend;
uv sync;
source .venv/bin/activate;
cd src;
python3 main.py;