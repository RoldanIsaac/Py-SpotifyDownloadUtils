import os
import sys
import zipfile
import tarfile
import rarfile  # You need to install it: pip install rarfile
from datetime import datetime

# Path to the unrar executable
rarfile.UNRAR_TOOL = r"C:\Program Files\UnRAR\UnRAR.exe"

# Path to the Documents folder (you can change it if needed)
if len(sys.argv) > 1:
    documents_folder = sys.argv[1]
else:
    documents_folder = os.path.expanduser("~/Documents")

# Supported compressed file extensions
compressed_exts = [".zip", ".rar", ".tar", ".tar.gz", ".tgz"]

# Create an output folder inside Documents to store extracted files
output_folder = os.path.join(documents_folder, "output")
os.makedirs(output_folder, exist_ok=True)

# Log file to keep track of extracted files and errors
log_file = os.path.join(output_folder, "extraction_log.txt")

# Open the log file in append mode so each run adds new entries
with open(log_file, "a", encoding="utf-8") as log:
    log.write("\n===== Extraction started at {} =====\n".format(datetime.now()))

    # Walk through the Documents folder (and its subfolders)
    for root, dirs, files in os.walk(documents_folder):
        for file in files:
            file_path = os.path.join(root, file)  # Full path of the file
            filename, ext = os.path.splitext(file)  # Split file name and extension

            # Check if the file is a supported compressed file
            if ext.lower() in compressed_exts or file.endswith(".tar.gz") or file.endswith(".tgz"):
                # Create a specific folder for this file inside extracted_files
                extract_dir = os.path.join(output_folder, filename)
                os.makedirs(extract_dir, exist_ok=True)

                try:
                    # If it's a ZIP file
                    if ext == ".zip":
                        with zipfile.ZipFile(file_path, "r") as zip_ref:
                            zip_ref.extractall(extract_dir)  # Extract all contents

                    # If it's a TAR, TAR.GZ, or TGZ file
                    elif ext in [".tar", ".gz", ".tgz", ".tar.gz"]:
                        with tarfile.open(file_path, "r:*") as tar_ref:
                            tar_ref.extractall(extract_dir)  # Extract all contents

                    # If it's a RAR file
                    elif ext == ".rar":
                        rarfile.UNRAR_TOOL = r"C:\Program Files\UnRAR\UnRAR.exe"
                        with rarfile.RarFile(file_path) as rar_ref:
                            rar_ref.extractall(extract_dir)  # Extract all contents

                    # Delete the original compressed file after successful extraction
                    os.remove(file_path)

                    # Print and log success
                    message = f"✅ Extracted & deleted: {file} → {extract_dir}\n"
                    print(message.strip())
                    log.write(message)

                except Exception as e:
                    # Print and log error (do NOT delete if failed)
                    message = f"❌ Error extracting {file}: {e}\n"
                    print(message.strip())
                    log.write(message)

    log.write("===== Extraction finished at {} =====\n".format(datetime.now()))
