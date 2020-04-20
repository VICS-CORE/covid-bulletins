#!/bin/bash

echo "Starting runner...", $(date)
pushd ~/Projects/covid-bulletins
git pull
python3 karnataka.py
git add .
git commit -m "daily update at $(date)"
git push origin master
popd
echo "Done"
