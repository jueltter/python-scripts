#!/usr/bin/env python3
import os
import sys

def list_files_sorted_by_size_in_gb(directory, output_file=None):
    """
    Lists all files in 'directory' (recursively) with:
      - File name
      - Absolute path
      - File size in GB
    Sorts the list by file size in ascending order (GB).
    
    Output is separated by tabs, printed to the console,
    and optionally written to a specified output file.
    """
    file_details = []

    # Walk through the directory and gather file data
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                size_bytes = os.path.getsize(filepath)
                size_gb = size_bytes / (1024 ** 3)  # convert bytes -> GB
                file_details.append((filename, filepath, size_gb))
            except OSError:
                # In case of any permission error or similar, skip that file
                continue

    # Sort by file size (ascending)
    file_details.sort(key=lambda x: x[2])

    # Build a list of output lines (tab-separated)
    # Header
    output_lines = ["File Name\tFile Path\tSize (GB)"]

    # Data lines
    for name, path, size_gb in file_details:
        output_lines.append(f"{name}\t{path}\t{size_gb:.2f}")

    # Convert lines to a single string
    final_output = "\n".join(output_lines)

    # 1) Print to console
    print(final_output)

    # 2) Optionally write to a file
    if output_file:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(final_output + "\n")
            print(f"\nResults have been written to: {output_file}")
        except OSError as e:
            print(f"ERROR: Could not write to {output_file}: {e}")

if __name__ == "__main__":
    # Usage:
    #   python list_files.py [directory] [output_file]
    # - directory: defaults to current directory if not provided
    # - output_file: if provided, script will write results to that file
    #
    # Examples:
    #   python list_files.py
    #   python list_files.py /path/to/dir
    #   python list_files.py /path/to/dir results.tsv

    if len(sys.argv) == 1:
        # No arguments -> current directory, no output file
        target_directory = "."
        output_file = None
    elif len(sys.argv) == 2:
        # One argument -> directory provided, no output file
        target_directory = sys.argv[1]
        output_file = None
    else:
        # Two or more arguments -> directory + output file
        target_directory = sys.argv[1]
        output_file = sys.argv[2]

    list_files_sorted_by_size_in_gb(target_directory, output_file)
