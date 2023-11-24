#!/bin/bash

# find $arg -type f -printf '%A@ %p\n' | sort -n | awk '{print $2}'
for arg in "$@"
do
  find $arg -type f -printf '%A@ %A+ %p\n' | sort --numeric-sort --reverse
done


