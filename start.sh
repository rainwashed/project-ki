#!/bin/sh

conda activate project-ki

python src/main.py & (cd src/view; npm run dev) & cd ../..