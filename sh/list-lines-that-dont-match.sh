#!/bin/bash

# Get the names of the two files
file1=$1
file2=$2

# Create a temporary file to store the lines that are not found in the second file
temp_file="/tmp/lines_not_found.txt"

# Iterate through the lines of the first file
while read -r line; do

    # Check if the line is found in the second file
    if ! grep -Fq "$line" "$file2"; then
        # If the line is not found in the second file, append it to the temporary file
        echo "$line" >> "$temp_file"
    fi

done < "$file1"

# Print the lines in the temporary file
cat "$temp_file"

# Remove the temporary file
rm "$temp_file"

