import subprocess
import sys
import os

# Folder paths
compressed_files_folder = r"C:\Users\Orlando\Downloads"
extracted_files_folder = r"C:\Users\Orlando\Downloads\extracted_files"

# String to remove from folder names
string_to_remove = "SpotiDownloader.com - "

# Scripts in the same folder
base_folder = os.path.dirname(os.path.abspath(__file__))
uncompress_script = os.path.join(base_folder, "uncompress.py")
rename_script = os.path.join(base_folder, "rename_folders.py")

try:
    # Run uncompress script with folder argument
    print("🚀 Running uncompress script...")
    subprocess.run([sys.executable, uncompress_script, compressed_files_folder], check=True)
    print("✅ Uncompress script finished.\n")

    # Run rename script with folder and string arguments
    print("🚀 Running rename script...")
    subprocess.run([sys.executable, rename_script, extracted_files_folder, string_to_remove], check=True)
    print("✅ Rename script finished.")

except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
