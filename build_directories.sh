#!/bin/bash
for i in {1..25}
do
    mkdir day_$i
    touch day_$i/day_$i.py
    cat python_boilerplate.py > day_$i/day_$i.py
    touch day_$i/test.txt
    touch day_$i/input.txt
done