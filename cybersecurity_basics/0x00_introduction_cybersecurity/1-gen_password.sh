#!/bin/bash
tr -dc '[:alnum:]' < /dev/urandom | head -c "${1:-20}" 2>/dev/null
