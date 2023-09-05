import os
import json
from datetime import datetime


"""
    Here you can map your file extensions to a folder
"""
# TODO: Regexes in SEED?
SEED = [
    ['images', ['png', 'gif', 'bmp', 'jpeg']],
    ['audio', ['mp3', 'wav']],
    ['src', ['cpp', 'h', 'c']],
    ['text', ['txt', 'doc']],
    ['archives', ['zip']]
]

OUTNAME = 'fs.generated.json'


def create_extension_map():
    """
        Returns a map of key extension and value category
        for efficient indexing
    """
    extension_to_category = {}

    for [category, extensions] in SEED:
        for extension in extensions:
            extension_to_category[extension] = category

    return extension_to_category


def allowed_walk(base: str, allowed_dirs: set[str]):
    """
        Generator for only walking through permissed directories 
    """
    for dirpath, dirnames, files in os.walk(base):
        if dirpath in allowed_dirs:
            yield (dirpath, dirnames, files)


def filter_files_by_category(files, ext_to_categories):
    for fname in files:
        extensions = fname.split('.')
        if len(extensions) == 1:
            continue

        extension = '.'.join(extensions[1:])
        if extension in ext_to_categories:
            yield (fname, extension)


def create_buckets(finfo, ext_to_categories):
    buckets = {cat: [] for cat in ext_to_categories.values()}
    for fname, fext in finfo:
        buckets[ext_to_categories[fext]].append(fname)
    # Erase categories with no files
    buckets = {key: value for key, value in buckets.items() if len(value) != 0}
    return buckets


def organize(allowed=[], base=os.curdir):
    ext_to_categories = create_extension_map()
    for dirpath, dirnames, files in allowed_walk(base, set(allowed)):
        buckets = create_buckets(
            filter_files_by_category(files, ext_to_categories),
            ext_to_categories)

        yield (dirpath, buckets)


def generate(allowed):
    today = datetime.today()
    script = {'org': {cat: files for (cat, files) in organize(allowed)}}
    script['date'] = today.strftime('%d/%m/%Y')
    script['timestamp'] = datetime.now().timestamp()
    return json.dumps(script)


with open(OUTNAME, 'w') as file:
    print(generate(['./myfiles', './myfiles/documents']), file=file)
