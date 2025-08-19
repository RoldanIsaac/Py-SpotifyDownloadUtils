import subprocess
import sys
import os

# Folder paths
compressed_files_folder = r"C:\Users\Orlando\Downloads"
output_folder = r"C:\Users\Orlando\Downloads\output"

# String to remove from folder names
string_to_remove = "SpotiDownloader.com - "

# Scripts in the same folder
base_folder = os.path.dirname(os.path.abspath(__file__))
uncompress_script = os.path.join(base_folder, "uncompress.py")
rename_folders_script = os.path.join(base_folder, "rename_folders.py")
rename_files_script = os.path.join(base_folder, "rename_files.py")

try:
    # Run uncompress script with folder argument
    print("🚀 Running uncompress script...")
    subprocess.run([sys.executable, uncompress_script, compressed_files_folder], check=True)
    print("✅ Uncompress script finished.\n")

    # Run rename folders script with folder and string arguments
    print("🚀 Running rename folder script...")
    subprocess.run([sys.executable, rename_folders_script, output_folder, string_to_remove], check=True)
    print("✅ Rename script finished.")

    # Run rename files script with folder and string arguments
    print("🚀 Running rename files script...")
    subprocess.run([sys.executable, rename_files_script, output_folder], check=True)
    print("✅ Rename script finished.")

except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
