#!/bin/bash

#Variale declaration
ENV=$1
FILE=$2

main() {
    python3 import_integration.py $ENV $FILE
}