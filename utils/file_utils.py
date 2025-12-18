
import os


def get_mp3_files_in_directory(directory):
    """
    Get all MP3 files in the given directory (not in subdirectories).
    
    Args:
        directory: Path to the directory to scan
        
    Returns:
        List of MP3 file paths
    """
    mp3_files = []
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            # Only get files (not directories) and only MP3 files
            if os.path.isfile(item_path) and item.lower().endswith('.mp3'):
                mp3_files.append(item_path)
    except Exception as e:
        print(f"❌ Error reading directory {directory}: {e}")
    
    return mp3_files


def get_album_folders(output_folder):
    """
    Get all subdirectories in the output folder (these are album folders).
    
    Args:
        output_folder: Path to the output directory
        
    Returns:
        List of album folder paths
    """
    album_folders = []
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"✅ Created output folder: {output_folder}")
            return album_folders
            
        for item in os.listdir(output_folder):
            item_path = os.path.join(output_folder, item)
            # Only get directories
            if os.path.isdir(item_path):
                album_folders.append(item_path)
    except Exception as e:
        print(f"❌ Error reading output folder {output_folder}: {e}")
    
    return album_folders


def get_mp3_files_in_album(album_folder):
    """
    Get all MP3 files inside an album folder.
    
    Args:
        album_folder: Path to the album folder
        
    Returns:
        List of MP3 file paths in the album
    """
    mp3_files = []
    try:
        for item in os.listdir(album_folder):
            item_path = os.path.join(album_folder, item)
            if os.path.isfile(item_path) and item.lower().endswith('.mp3'):
                mp3_files.append(item_path)
    except Exception as e:
        print(f"❌ Error reading album folder {album_folder}: {e}")
    
    return mp3_files