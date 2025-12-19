import os
import sys
import json

# === Configuration ===
# Get folder path and strings to remove from command line arguments
if len(sys.argv) > 1:
    parent_dir = sys.argv[1]
else:
    parent_dir = os.path.expanduser("~/Documents")

if len(sys.argv) > 2:
    try:
        # Try to parse as JSON array
        strings_to_remove = json.loads(sys.argv[2])
        if not isinstance(strings_to_remove, list):
            strings_to_remove = [strings_to_remove]
    except json.JSONDecodeError:
        # If not valid JSON, treat as single string for backwards compatibility
        strings_to_remove = [sys.argv[2]]
else:
    strings_to_remove = []

# Walk the directory tree from the bottom up (so we rename child folders before parent folders)
for root, dirs, files in os.walk(parent_dir, topdown=False):
    for dir_name in dirs:
        new_name = dir_name
        renamed = False
        
        # Remove each string from the folder name
        for remove_str in strings_to_remove:
            if remove_str in new_name:
                new_name = new_name.replace(remove_str, "")
                renamed = True
        
        # Only rename if something was changed
        if renamed:
            old_path = os.path.join(root, dir_name)
            new_path = os.path.join(root, new_name)

            try:
                # Rename the folder
                os.rename(old_path, new_path)
                print(f"✅ Renamed: {old_path} → {new_path}")
            except Exception as e:
                print(f"❌ Error renaming {old_path}: {e}")
