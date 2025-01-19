#!/usr/bin/env python3
import sys
import os

def extract_unique_extensions(input_file, output_file):
    """
    Reads a tab-separated file (3 columns), extracts the file extension
    from column 1, and writes only unique extensions to output_file,
    one per line.

    - If a filename has no dot, it is treated as "no extension".
    - By default, extensions are sorted alphabetically in the output.
      (If you want them in the order encountered, see the 'alternative
       approach' comment below.)
    """
    extensions_found = set()

    # 1) Read the input file and collect extensions in a set
    with open(input_file, 'r', encoding='utf-8') as f_in:
        for line in f_in:
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t')
            # The first column is the filename
            filename = parts[0]

            # Use os.path.splitext to separate the extension
            root, ext = os.path.splitext(filename)

            if ext:
                # If you want to remove the leading dot, uncomment:
                # ext = ext.lstrip('.')
                extensions_found.add(ext)
            else:
                extensions_found.add("no extension")

    # 2) Write unique extensions to the output file
    # Sort them so we don't get random order from the set
    unique_sorted_extensions = sorted(extensions_found)

    with open(output_file, 'w', encoding='utf-8') as f_out:
        for extension in unique_sorted_extensions:
            f_out.write(extension + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python unique_extensions.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    extract_unique_extensions(input_file, output_file)
    print(f"Unique extensions have been written to: {output_file}")
