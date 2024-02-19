#!/bin/bash
delay=$((RANDOM % 180))
sleep $delay
~/swimcheck/venv/bin/python ~/swimcheck/daily_summary.py