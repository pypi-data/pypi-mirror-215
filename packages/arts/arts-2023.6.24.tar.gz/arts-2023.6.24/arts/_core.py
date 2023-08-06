import os
from os.path import abspath


def get_readme_files(folder):
    result = []
    fodeep = len(abspath(folder))
    for root, dirs, files in os.walk(folder):
        for x in files:
            if 'readme.md' in x.lower():
                relative_path = abspath(f"{root}/{x}")[fodeep:].replace('\\', '/')
                result.append(relative_path)
                break
    return result