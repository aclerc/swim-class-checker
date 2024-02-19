#!/bin/bash
delay=$((RANDOM % 300))
sleep $delay
~/swimcheck/venv/bin/python ~/swimcheck/check_for_places.py