#!/bin/bash

for file in *.py
do
    echo $file
    yapf "$file" > "_y$file"
    cp "_y$file" "$file"
    rm "_y$file"
done
