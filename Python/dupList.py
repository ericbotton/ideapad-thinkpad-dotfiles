#! /env/bin/python3
""" module """

import os
import hashlib

def find_duplicates(dir1, dir2):
    """ function """
    duplicates = []
    dir1_files = {}
    dir2_files = {}

    for root, dirs, files in os.walk(dir1):
        for file in files:
            path = os.path.join(root, file)
            with open(path, 'rb') as f:
                hash = hashlib.md5(f.read()).hexdigest()
                dir1_files[hash] = path

    for root, dirs, files in os.walk(dir2):
        for file in files:
            path = os.path.join(root, file)
            with open(path, 'rb') as f:
                hash = hashlib.md5(f.read()).hexdigest()
                dir2_files[hash] = path

    for hash in dir1_files:
        if hash in dir2_files:
            duplicates.append((dir1_files[hash], dir2_files[hash]))

    return duplicates
