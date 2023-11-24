#!/bin/bash

dir1="$1"
dir2="$2"

find $dir1 -type f | while read file1; do
    hash1=$(md5sum "$file1" | cut -d " " -f 1)
    find $dir2 -type f | while read file2; do
        hash2=$(md5sum "$file2" | cut -d " " -f 1)
        if [ "$hash1" == "$hash2" ]; then
            echo "Duplicate: $file1 and $file2"
        fi
    done
done
