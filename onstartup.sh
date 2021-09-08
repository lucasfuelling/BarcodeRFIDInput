#!/bin/bash
cd ~/BarcodeRFIDInput
echo "wait for wifi"
sleep 10
git pull
python3 main.py
