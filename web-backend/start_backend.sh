#!/bin/zsh

conda activate open-tcm

# Start the Flask server with pm2
pm2 start run.py --name "opentcm-backend" --interpreter python
