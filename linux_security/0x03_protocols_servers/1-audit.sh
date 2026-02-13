#!/bin/bash
grep -Ev '^\s*#' /etc/ssh/sshd_config | grep -E 'Include|PasswordAuthentication'
