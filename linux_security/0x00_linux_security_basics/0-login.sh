#!/bin/bash
sudo last -F -n 5 -i | grep "$1"
