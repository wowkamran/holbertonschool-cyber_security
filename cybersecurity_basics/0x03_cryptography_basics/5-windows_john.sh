#!/bin/bash
john --format=nt --wordlist=/usr/share/wordlists/rockyou.txt "$1"
john --show --format=nt "$1" | cut -d ":" -f 2 > 5-password.txt
