# This script reads the JSON generated by gen.py and applies it

import json
import os
import shutil
from pprint import pprint

OUTNAME = 'fs.generated.json'


def read_file():
    with open(OUTNAME, 'r') as file:
        return json.load(file)


def apply(fsmap):
    org = fsmap['org']

    for basedir, categories in org.items():
        for category, files in categories.items():
            path_to_category = f'{basedir}/{category}'

            # Create the subdirectory if it does not already exist
            if not os.path.isdir(path_to_category):
                os.mkdir(path_to_category)

            # Move the organized files into the categorized subdiretories:
            for file in files:
                # Source path:
                base_path_to_file = f'{basedir}/{file}'
                # Destination path:
                moved_file_path = f'{path_to_category}/{file}'

                # If there is already a file at the destination, then
                # the user has most likely ran this script twice
                if os.path.isfile(moved_file_path):
                    continue

                # Move the file from its original position to be inside the category
                if os.path.isfile(base_path_to_file):
                    shutil.move(base_path_to_file, moved_file_path)
                else:
                    print(f'{base_path_to_file} does not exist.')


apply(fsmap=read_file())
