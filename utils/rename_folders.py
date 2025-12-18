import os
import sys

# === Configuration ===
# Get folder path and string to remove from command line arguments
if len(sys.argv) > 1:
    parent_dir = sys.argv[1]
else:
    parent_dir = os.path.expanduser("~/Documents")

if len(sys.argv) > 2:
    remove_str = sys.argv[2]
else:
    remove_str = ""

# Walk the directory tree from the bottom up (so we rename child folders before parent folders)
for root, dirs, files in os.walk(parent_dir, topdown=False):
    for dir_name in dirs:
        if remove_str in dir_name:
            old_path = os.path.join(root, dir_name)
            new_name = dir_name.replace(remove_str, "")
            new_path = os.path.join(root, new_name)

            try:
                # Rename the folder
                os.rename(old_path, new_path)
                print(f"✅ Renamed: {old_path} → {new_path}")
            except Exception as e:
                print(f"❌ Error renaming {old_path}: {e}")
