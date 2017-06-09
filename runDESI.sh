#!/bin/bash
echo "Starting"
cd ~/Desktop/Sentinel
git pull
echo "Pulling"
sudo python3 ~/Desktop/Sentinel/MissionControl.py && sudo python3 ~/Desktop/Sentinel/triggers/alexaSnow.py resources/DESI.pmdl
