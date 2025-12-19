import os
import sys
import shutil
import json
from pathlib import Path
from Metatags import getTagField
from file_utils import get_album_folders, get_mp3_files_in_album, get_mp3_files_in_directory



def check_if_belongs_to_album(file_path, album_folder):
    """
    Check if a file belongs to an album by comparing artist and album tags.
    
    Args:
        file_path: Path to the MP3 file to check
        album_folder: Path to the album folder
        
    Returns:
        True if the file belongs to the album, False otherwise
    """
    try:
        # Get files in the album folder
        album_files = get_mp3_files_in_album(album_folder)
        
        if not album_files:
            return False
        
        # Get artist and album from the file to check
        file_artist = getTagField(file_path, 0)  # 0 = Artist
        file_album = getTagField(file_path, 1)   # 1 = Album
        
        # Get artist and album from one of the files in the album folder
        # (we assume all files in the album folder have the same artist and album)
        album_artist = getTagField(album_files[0], 0)
        album_name = getTagField(album_files[0], 1)
        
        # Compare artist and album
        if file_artist == album_artist and file_album == album_name:
            return True
        
        return False
        
    except Exception as e:
        print(f"⚠️  Error checking if file belongs to album: {e}")
        return False


def remove_strings_from_filename(file_path, strings_to_remove):
    """
    Remove multiple strings from the filename.
    
    Args:
        file_path: Path to the file
        strings_to_remove: List of strings to remove from the filename
        
    Returns:
        New filename (not full path, just the filename)
    """
    filename = os.path.basename(file_path)
    new_filename = filename
    
    # Remove each string from the filename
    for string_to_remove in strings_to_remove:
        new_filename = new_filename.replace(string_to_remove, "")
    
    return new_filename


def process_loose_files(source_folder, output_folder, strings_to_remove):
    """
    Process loose MP3 files: remove strings from filename and move to output folder.
    If the file belongs to an existing album, move it to that album folder.
    
    Args:
        source_folder: Folder containing the loose MP3 files
        output_folder: Folder where files should be moved
        strings_to_remove: List of strings to remove from filenames
    """
    print(f"🔍 Scanning for loose MP3 files in: {source_folder}")
    
    # Get all MP3 files in the source folder (not in subdirectories)
    mp3_files = get_mp3_files_in_directory(source_folder)
    
    if not mp3_files:
        print("ℹ️  No loose MP3 files found.")
        return
    
    print(f"📁 Found {len(mp3_files)} loose MP3 file(s)")
    
    # Get all album folders in the output folder
    album_folders = get_album_folders(output_folder)
    print(f"📂 Found {len(album_folders)} album folder(s) in output directory")
    
    # Process each MP3 file
    for file_path in mp3_files:
        try:
            original_filename = os.path.basename(file_path)
            print(f"\n🎵 Processing: {original_filename}")
            
            # Remove strings from filename
            new_filename = remove_strings_from_filename(file_path, strings_to_remove)
            
            # Check if file belongs to any existing album
            destination_folder = output_folder
            album_found = False
            
            for album_folder in album_folders:
                if check_if_belongs_to_album(file_path, album_folder):
                    destination_folder = album_folder
                    album_found = True
                    album_name = os.path.basename(album_folder)
                    print(f"   ✅ Belongs to album: {album_name}")
                    break
            
            if not album_found:
                print(f"   ℹ️  Does not belong to any existing album, moving to output root")
            
            # Create destination path
            destination_path = os.path.join(destination_folder, new_filename)
            
            # Check if file already exists at destination
            if os.path.exists(destination_path):
                print(f"   ⚠️  File already exists at destination: {new_filename}")
                continue
            
            # Move the file
            shutil.move(file_path, destination_path)
            print(f"   ✅ Moved to: {destination_path}")
            
        except Exception as e:
            print(f"   ❌ Error processing {original_filename}: {e}")
    
    print("\n✅ Processing complete!")


if __name__ == "__main__":
    # Check if arguments are provided
    if len(sys.argv) < 3:
        print("Usage: python process_loose_files.py <source_folder> <output_folder> [strings_to_remove_json]")
        sys.exit(1)
    
    source_folder = sys.argv[1]
    output_folder = sys.argv[2]
    
    # Parse strings_to_remove from JSON array or use empty list
    if len(sys.argv) > 3:
        try:
            strings_to_remove = json.loads(sys.argv[3])
            if not isinstance(strings_to_remove, list):
                strings_to_remove = [strings_to_remove]
        except json.JSONDecodeError:
            # If not valid JSON, treat as single string for backwards compatibility
            strings_to_remove = [sys.argv[3]]
    else:
        strings_to_remove = []
    
    # Validate that source folder exists
    if not os.path.exists(source_folder):
        print(f"❌ Error: Source folder does not exist: {source_folder}")
        sys.exit(1)
    
    # Process the files
    process_loose_files(source_folder, output_folder, strings_to_remove)
