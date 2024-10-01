#!/bin/bash

# Определяем директорию, где находится этот скрипт
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Определяем путь к виртуальному окружению и Python
PYTHON_PATH="$SCRIPT_DIR/.venv/bin/python3"

# Определяем путь к Python-скрипту, который нужно запустить
SCRIPT_PATH="$SCRIPT_DIR/src/parser/main.py"


export PYTHONPATH="/home/tminww/kapibara/backend"

source $SCRIPT_DIR/.venv/bin/activate
$PYTHON_PATH $SCRIPT_PATH
