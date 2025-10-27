# python
import os
from collections import defaultdict

RAW_FILE = 'file_names_raw.txt'
BASE_FILE = 'file_names_without_path.txt'

def list_files(path):
    files = []

    for root, dirs, filenames in os.walk(path):
        for fname in filenames:
            files.append(os.path.join(root, fname))
    return files

def write_lines(path, lines):
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

def find_duplicates_by_basename(full_paths):
    groups = defaultdict(list)
    for p in full_paths:
        groups[os.path.basename(p)].append(p)
    # return only basenames that have more than one path
    return {name: paths for name, paths in groups.items() if len(paths) > 1}

def check_content_duplicate(duplicate_paths):
    with open(duplicate_paths[0], 'rb') as f:
        reference_content = f.read()
    for path in duplicate_paths[1:]:
        with open(path, 'rb') as f:
            content = f.read()
        if content == reference_content:
            return duplicate_paths
    return None




# main flow
all_files = list_files('C:/Users/Liam')
write_lines(RAW_FILE, all_files)
base_names = [os.path.basename(p) for p in all_files]
write_lines(BASE_FILE, base_names)

duplicates = find_duplicates_by_basename(all_files)
for name, paths in duplicates.items():
    # print only once per duplicate group
    with open('duplicates_report.txt', 'a', encoding='utf-8') as report:
        content_duplicates = str(check_content_duplicate(paths))

        report.write(content_duplicates + '\n')


