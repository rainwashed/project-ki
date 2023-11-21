#!/bin/bash
find ./src/{audio,conversation,server} ./src/{main,run}.py -name '*.py' | xargs wc -l