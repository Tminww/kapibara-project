#!/bin/bash
SCRIPT_DIR=$(pwd)
BASE_DIR=$(dirname $SCRIPT_DIR)
BACKEND_DIR="$BASE_DIR/backend"
echo $BACKEND_DIR 
cd $BACKEND_DIR
source .venv/bin/activate
cd "$BACKEND_DIR/src/"
echo $(pwd)
echo $(which python3)
python3 -m scripts.run_scheduler_task 
