#!/bin/bash
echo "Starting"
runclean && sudo python3 ~/Desktop/Sentinel/triggers/alexaSnow.py resources/DESI.pmdl
