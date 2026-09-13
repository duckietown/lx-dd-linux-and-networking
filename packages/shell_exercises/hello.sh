#!/usr/bin/env bash

# Change only the text between the quotation marks.
message="<WRITE A GREETING HERE>"

# `%s` inserts the message and `\n` ends the line on standard output.
printf '%s\n' "$message"
