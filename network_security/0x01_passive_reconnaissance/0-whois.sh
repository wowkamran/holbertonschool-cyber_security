#!/bin/bash
whois $1 | awk 'BEGIN{FS=": *"} /Registrant|Admin|Tech/ && /(Name|Organization|Street|City|State|Postal|Country|Phone|Phone Ext|Email)/{if($1~/Street/){print $1","$2" "}else if($1~/Phone Ext/){print $1":,"}else{print $1","$2}}'
