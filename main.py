import subprocess
import sys
import os

# Folder paths
compressed_files_folder = r"C:\Users\Administrator\Downloads"
output_folder = r"C:\Users\Administrator\Downloads\output"

# String to remove from folder names
string_to_remove = "SpotiDownloader.com - "

# Scripts in the same folder
base_folder = os.path.dirname(os.path.abspath(__file__))
uncompress_script = os.path.join(base_folder, "utils/uncompress.py")
process_loose_files_script = os.path.join(base_folder, "utils/process_loose_files.py")
rename_folders_script = os.path.join(base_folder, "utils/rename_folders.py")
rename_files_script = os.path.join(base_folder, "utils/rename_files.py")
add_album_year_script = os.path.join(base_folder, "utils/add_album_year.py")

try:
    # Run uncompress script with folder argument
    print("🚀 Running uncompress script...")
    subprocess.run([sys.executable, uncompress_script, compressed_files_folder], check=True)
    print("✅ Uncompress script finished.\n")

    # Run process loose files script
    print("🚀 Running process loose files script...")
    subprocess.run([sys.executable, process_loose_files_script, compressed_files_folder, output_folder, string_to_remove], check=True)
    print("✅ Process loose files script finished.\n")

    # Run rename folders script with folder and string arguments
    print("🚀 Running rename folder script...")
    subprocess.run([sys.executable, rename_folders_script, output_folder, string_to_remove], check=True)
    print("✅ Rename script finished.")

    # Run rename files script with folder and string arguments
    print("🚀 Running rename files script...")
    subprocess.run([sys.executable, rename_files_script, output_folder], check=True)
    print("✅ Rename script finished.")

    # Run add album year script
    print("🚀 Running add album year script...")
    subprocess.run([sys.executable, add_album_year_script, output_folder], check=True)
    print("✅ Add album year script finished.")

except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
