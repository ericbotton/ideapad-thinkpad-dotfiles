#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Usage: $0 directory1 directory2"
  exit 1
fi

dir1=$1
dir2=$2

find "$dir1" -type f -print -exec bash -c '
  file1="$1"
  file2="${file1/$1/$2}"

  if [ -f "$file2" ]; then
    cmp -s "$file1" "$file2"
    if [ $? -ne 0 ]; then
      vimdiff "$file1" "$file2"
    fi
  fi
' -- {} "$dir2" \;

<<explainer
Here\'s the bash script that takes two directories as arguments, iterates through each directory and sub-directory recursively, compares each text file, and runs vimdiff on files that differ 


Here\'s the bash script that takes two directories as arguments, iterates through each directory and sub-directory recursively, compares each text file, and runs vimdiff on files that differ:

Bash
#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Usage: $0 directory1 directory2"
  exit 1
fi

dir1=$1
dir2=$2

find "$dir1" -type f -exec bash -c \'
  file1="$1"
  file2="${file1/$1/$2}"

  if [ -f "$file2" ]; then
    cmp -s "$file1" "$file2"
    if [ $? -ne 0 ]; then
      vimdiff "$file1" "$file2"
    fi
  fi
\' -- {} "$dir2" \;
Use code with caution. Learn more
This script first checks if two arguments are provided. If not, it displays an error message and exits. Otherwise, it assigns the first argument to dir1 and the second argument to dir2.

The find command is used to recursively search for regular files in dir1. For each file found, a bash command is executed using bash -c. The file path is passed as an argument to the bash command.

Inside the bash command, the file path in dir2 is constructed by replacing dir1 with dir2 in the file path. Then, the cmp command is used to compare the two files. If the files are different, vimdiff is used to compare and merge the files.
explainer
