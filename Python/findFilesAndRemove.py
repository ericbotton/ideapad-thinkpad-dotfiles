#!/usr/bin/python3

import os
import re
""" find files matching pattern in a directory (recursively) """ 
"""    and ask to delete """

def recursive_search(directory, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if re.search(pattern, filename):
                matches.append(os.path.join(root, filename))
    return matches

def delete_files(files):
    for file in files:
        delete = input(f"Do you want to delete {file}? (y/n): ")
        if delete.lower() == 'y' or delete.lower() == "yes":
            os.remove(file)
            print(f"{file} deleted.")
        else:
            print(f"{file} not deleted.")

directory = input("Enter the directory to search: ")
pattern = input("Enter the pattern to search for: ")

matches = recursive_search(directory, pattern)
print("Files found:")
for match in matches:
    print(match)

delete_files(matches)
