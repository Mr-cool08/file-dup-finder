# python
import argparse
import os
import sys
from collections import defaultdict

RAW_FILE = 'file_names_raw.txt'
BASE_FILE = 'file_names_without_path.txt'


def print_progress(count, total, prefix='', bar_length=40):
    """Print a simple progress bar to the console."""
    if total <= 0:
        return
    filled_len = int(round(bar_length * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_length - filled_len)
    sys.stdout.write("\r{} [{}] {}% ({}/{})".format(prefix, bar, percents, count, total))
    sys.stdout.flush()
    if count == total:
        sys.stdout.write('\n')


def list_files(path):
    # first pass: count total files so we can show progress
    total = 0
    for _root, _dirs, filenames in os.walk(path):
        total += len(filenames)

    files = []
    counted = 0
    print_progress(0, total, prefix='Scanning files')

    for root, dirs, filenames in os.walk(path):
        for fname in filenames:
            files.append(os.path.join(root, fname))
            counted += 1
            print_progress(counted, total, prefix='Scanning files')
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
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find duplicate files by basename and content')
    parser.add_argument('path', nargs='?', default=r'Z:/files', help='Root path to scan (default: Z:/files)')
    args = parser.parse_args()

    target = args.path

    # ensure the duplicates report is empty at start
    open('duplicates_report.txt', 'w', encoding='utf-8').close()

    all_files = list_files(target)
    write_lines(RAW_FILE, all_files)
    base_names = [os.path.basename(p) for p in all_files]
    write_lines(BASE_FILE, base_names)

    duplicates = find_duplicates_by_basename(all_files)
    for name, paths in duplicates.items():
        # print only once per duplicate group
        with open('duplicates_report.txt', 'a', encoding='utf-8') as report:
            content_duplicates = str(check_content_duplicate(paths))

            report.write(content_duplicates + '\n')
