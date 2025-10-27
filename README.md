dupfinder
========

Simple duplicate-file finder script (by basename + content).

What this does
--------------
- Scans a directory tree and records every file found.
- Detects files that share the same basename (filename without path).
- For basename matches, compares file content (byte-for-byte) and reports groups where at least two files have identical content.

Requirements
------------
- Python 3.6+ (tested on Python 3.8+)
- No external packages required.

Files produced
--------------
- `file_names_raw.txt` - full paths of every file found (one per line).
- `file_names_without_path.txt` - just the basenames (one per line).
- `duplicates_report.txt` - a report written by the script. Each line is either `None` or a Python-style list of paths (as produced by the script's internal `str(...)`) for groups where duplicate content was detected.

Notes about `duplicates_report.txt`
----------------------------------
- The script groups files by basename, then for each group it compares the bytes of the first file with the others.
- If a matching file is found, the script writes the Python string representation of the list of paths for that group to `duplicates_report.txt`.
- If no content-match is found for a group, the script writes `None` for that group.

Usage (Windows - cmd.exe)
-------------------------
Open a command prompt and run one of the following commands from the project directory or give an absolute/relative target path.

Run with the default hardcoded path (the script defaults to `Z:/files`):

```cmd
python main.py
```

Run and scan a specific folder (example):

```cmd
python main.py "D:\\MyDocuments"
```

Behavior and examples
---------------------
- The script prints a simple progress bar while scanning files.
- After the run you can open `duplicates_report.txt` to see which basename groups included identical files.

Limitations and improvements
----------------------------
- Current content comparison reads entire files into memory. That can be heavy for large files. Consider using a hashing approach (e.g. SHA-256) or a streaming chunked compare to reduce memory use.
- The script only compares files that share the exact same basename. Files with different names but identical content are not reported.
- The duplicates report format is minimal (uses `str(list)` and `None`). If you plan to parse the output programmatically, consider modifying the script to write JSON (e.g. use the `json` module) or another structured format.
- No exclude patterns, no symlink handling options, and no multithreading; these could be added later.

Next steps (optional)
---------------------
- Replace byte-for-byte comparisons with a two-pass approach: first compute hashes, then verify by byte-compare when hashes match.
- Add command-line flags for verbosity, exclusion patterns, follow-symlinks, and output format (JSON/CSV).

License
-------
- Use as you wish. No license specified.

Contact / Help
--------------
If you want me to update the script to output JSON, use hashing for large files, or add CLI flags, tell me which feature and I'll implement it.

