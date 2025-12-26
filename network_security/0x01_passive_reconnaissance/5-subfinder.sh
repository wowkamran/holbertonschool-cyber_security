#!/bin/bash
subfinder -d $1 -silent -ip | awk '{print $1","$2}' > $1.txt
