import os
import shutil

SEED = [
    ['images', ['png', 'gif', 'bmp', 'jpeg']],
    ['audio', ['mp3', 'wav']],
    ['c_code', ['cpp', 'h', 'c']],
    ['archives', ['zip']]
]


def create_extension_map():
    extension_to_category = {}

    for [category, extensions] in SEED:
        for extension in extensions:
            extension_to_category[extension] = category

    return extension_to_category


def allowed_walk(base, allowed_dirs):
    for dirpath, dirnames, files in os.walk(base):
        if dirpath in allowed_dirs:
            yield (dirpath, dirnames, files)


def categorize_files(files, ext_to_categories):
    for fname in files:
        extensions = fname.split('.')
        if len(extensions) == 1:
            continue

        extension = '.'.join(extensions[1:])
        if extension in ext_to_categories:
            yield (fname, extension)


def organize(allowed=[], base=os.curdir):
    ext_to_categories = create_extension_map()
    for dirpath, dirnames, files in allowed_walk(base, set(allowed)):
        # Select only the files which can be organized
        finfo = categorize_files(files, ext_to_categories)

        buckets = {cat: [] for cat in ext_to_categories.values()}

        for fname, fext in finfo:
            buckets[ext_to_categories[fext]].append(fname)

        print(buckets)


organize(['./myfiles'])
