from Metatags import loadAudio, getAudioTag
import loadFolder
from pathlib import Path
import sys
import os

# === Configuration ===
# Get folder path and string to remove from command line arguments
if len(sys.argv) > 1:
    parent_dir = sys.argv[1]
else:
    parent_dir = os.path.expanduser("~/Documents")

# Walk the directory tree from the bottom up
for root, dirs, files in os.walk(parent_dir, topdown=False):
    for dir_name in dirs:

        # Get album path from the iteration
        album_path = os.path.join(root, dir_name)
        # print(album_path)
 
        # Get all files in folder
        folder = loadFolder.Folder(album_path, '.mp3')
        folder.init()

        for index, file_path in enumerate(folder.filesPath):
            try:
                # Load audio
                audio_file = loadAudio(file_path)

                # Get metadata
                audio_tag = getAudioTag(audio_file)
                track_number = audio_tag[3].count

                # Format track number
                track_str = f"{track_number:02d}"
             
                # 0 → carácter de relleno (usa ceros)
                # 2 → ancho mínimo (2 caracteres)
                # d → tipo decimal (entero)

                # Construct paths 
                original_path = Path(album_path) / folder.files[index]
                new_filename = f"{track_str}. {folder.files[index]}"
                new_path = Path(album_path) / new_filename

                # Validate before renaming
                if original_path.exists():
                    if not new_path.exists():
                        original_path.rename(new_path)
                        # print(f"✅ Renamed: {original_path} -> {new_path.name}")
                    else: 
                        print(f"❌ Error: File already exists: {new_path}")
                else:
                    print(f"❌ Error: Original file not found: {original_path}")

            except Exception as e:
                print(f"❌ Error processing file {file_path}: {str(e)}")
                continue
                
        
            