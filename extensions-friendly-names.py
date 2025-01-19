#!/usr/bin/env python3

import sys
import winreg

def get_friendly_name(class_name):
    """
    Given a class name (e.g., "txtfile"), look in HKEY_CLASSES_ROOT\<className>
    for a 'FriendlyTypeName' or default value. Return whatever we find as a string.
    """
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, class_name) as class_key:
            # Try 'FriendlyTypeName' first
            try:
                friendly_type, _ = winreg.QueryValueEx(class_key, "FriendlyTypeName")
                if friendly_type:
                    # Many FriendlyTypeName values are resource references (e.g. "@%SystemRoot%\\system32\\..."),
                    # we simply return them as-is. 
                    return friendly_type
            except FileNotFoundError:
                pass
            
            # If that doesn't exist, fall back to the default value
            try:
                default_value, _ = winreg.QueryValueEx(class_key, None)
                if default_value:
                    return default_value
            except FileNotFoundError:
                pass
    except OSError:
        pass
    
    return None

def main():
    # If desired, you can allow a command-line argument for the output filename.
    # For simplicity, we'll just hard-code it here:
    output_file = "extensions-friendly-names.txt"
    
    # Open HKEY_CLASSES_ROOT
    try:
        root_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "")
    except OSError as e:
        print(f"Error: Cannot open HKEY_CLASSES_ROOT. {e}")
        sys.exit(1)
    
    # Collect (extension, friendly_name) pairs
    results = []
    
    index = 0
    while True:
        try:
            # Enumerate subkeys
            subkey_name = winreg.EnumKey(root_key, index)
            index += 1
            
            # Check if this subkey is an extension (begins with '.')
            if subkey_name.startswith('.'):
                extension = subkey_name  # e.g., ".txt"
                
                # Open the extension key to retrieve the default class
                try:
                    with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, subkey_name) as ext_key:
                        default_class, _ = winreg.QueryValueEx(ext_key, None)  # e.g., "txtfile"
                except (FileNotFoundError, OSError):
                    default_class = None
                
                # Resolve friendly name if we have a default class
                friendly_name = None
                if default_class:
                    friendly_name = get_friendly_name(default_class)
                
                # Store the tuple (extension, friendly_name or "(none)")
                results.append((extension, friendly_name if friendly_name else "(none)"))
        except OSError:
            # No more subkeys to enumerate
            break
    
    # Sort results by extension (optional, but usually helpful)
    results.sort(key=lambda x: x[0].lower())
    
    # Write the results to a 2-column file
    # We'll use a tab character between columns; you can use commas, etc., if you prefer
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            # Optionally, write a header line
            f.write("Extension\tFriendly Name\n")
            for ext, fname in results:
                f.write(f"{ext}\t{fname}\n")
        
        print(f"Export complete. Results written to '{output_file}'.")
    except OSError as e:
        print(f"Error writing to '{output_file}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
