import os
import sys
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time
from Metatags import getTagField
from file_utils import get_mp3_files_in_album

def get_mp3_files_in_folder(folder_path):
    """
    Get all MP3 files in a folder.
    
    Args:
        folder_path: Path to the folder
        
    Returns:
        List of MP3 file paths
    """
    mp3_files = []
    try:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path) and item.lower().endswith('.mp3'):
                mp3_files.append(item_path)
    except Exception as e:
        print(f"❌ Error reading folder {folder_path}: {e}")
    
    return mp3_files


def get_album_info_from_tags(album_folder):
    """
    Get artist and album name from MP3 tags in the folder.
    
    Args:
        album_folder: Path to the album folder
        
    Returns:
        Tuple (artist, album_name) or (None, None) if not found
    """
    try:
        mp3_files = get_mp3_files_in_folder(album_folder)
        
        if not mp3_files:
            return None, None
        
        # Get artist and album from the first MP3 file
        artist = getTagField(mp3_files[0], 0)  # 0 = Artist
        album_name = getTagField(mp3_files[0], 1)  # 1 = Album
        
        return artist, album_name
        
    except Exception as e:
        print(f"⚠️  Error getting album info from tags: {e}")
        return None, None


def search_wikipedia_album_year(artist, album_name):
    """
    Search Wikipedia for album release year.
    
    Args:
        artist: Artist name
        album_name: Album name
        
    Returns:
        Year as integer or None if not found
    """
    try:
        # Clean up search terms
        search_query = f"{album_name} {artist} album"
        
        # Search Wikipedia
        search_url = f"https://en.wikipedia.org/w/api.php"
        params = {
            "action": "opensearch",
            "search": search_query,
            "limit": 5,
            "namespace": 0,
            "format": "json"
        }
        
        response = requests.get(search_url, params=params, timeout=10)
        results = response.json()
        
        if len(results) < 4 or not results[3]:
            return None
        
        # Try each result
        for page_url in results[3]:
            time.sleep(0.5)  # Be respectful to Wikipedia
            
            # Get page content
            page_response = requests.get(page_url, timeout=10)
            soup = BeautifulSoup(page_response.content, 'html.parser')
            
            # Look for infobox (common in album pages)
            infobox = soup.find('table', class_='infobox')
            
            if infobox:
                # Look for "Released" row
                rows = infobox.find_all('tr')
                for row in rows:
                    th = row.find('th')
                    if th and 'released' in th.get_text().lower():
                        td = row.find('td')
                        if td:
                            text = td.get_text()
                            # Extract year (4 digits)
                            year_match = re.search(r'\b(19\d{2}|20\d{2})\b', text)
                            if year_match:
                                year = int(year_match.group(1))
                                # Validate year (must be between 1900 and current year)
                                if 1900 <= year <= 2025:
                                    print(f"   📚 Wikipedia: Found year {year}")
                                    return year
        
        return None
        
    except Exception as e:
        print(f"   ⚠️  Wikipedia search error: {e}")
        return None


def search_aoty_album_info(artist, album_name):
    """
    Search AOTY (Album of the Year) for album year and genre.
    
    Args:
        artist: Artist name
        album_name: Album name
        
    Returns:
        Tuple (year, genre) or (None, None) if not found
    """
    try:
        # Clean up search terms for URL
        search_query = f"{artist} {album_name}".lower()
        search_query = re.sub(r'[^\w\s]', '', search_query)
        search_query = search_query.replace(' ', '+')
        
        # Search AOTY
        search_url = f"https://www.albumoftheyear.org/search/albums/?q={search_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for album results
        album_blocks = soup.find_all('div', class_='albumBlock')
        
        for block in album_blocks[:3]:  # Check first 3 results
            try:
                # Get album title and artist from result
                title_elem = block.find('div', class_='albumTitle')
                artist_elem = block.find('div', class_='artistTitle')
                
                if not title_elem or not artist_elem:
                    continue
                
                result_album = title_elem.get_text().strip().lower()
                result_artist = artist_elem.get_text().strip().lower()
                
                # Check if it matches (fuzzy match)
                if (album_name.lower() in result_album or result_album in album_name.lower()) and \
                   (artist.lower() in result_artist or result_artist in artist.lower()):
                    
                    # Get the album page URL
                    link = block.find('a', href=True)
                    if link:
                        album_url = "https://www.albumoftheyear.org" + link['href']
                        time.sleep(0.5)
                        
                        # Get album page
                        album_response = requests.get(album_url, headers=headers, timeout=10)
                        album_soup = BeautifulSoup(album_response.content, 'html.parser')
                        
                        # Extract year
                        year_elem = album_soup.find('div', class_='date')
                        year = None
                        if year_elem:
                            year_text = year_elem.get_text()
                            year_match = re.search(r'\b(19\d{2}|20\d{2})\b', year_text)
                            if year_match:
                                year = int(year_match.group(1))
                                if 1900 <= year <= 2025:
                                    print(f"   🎵 AOTY: Found year {year}")
                        
                        # Extract genre
                        genre = None
                        genre_elem = album_soup.find('div', class_='type')
                        if genre_elem:
                            genre = genre_elem.get_text().strip()
                            print(f"   🎸 AOTY: Found genre {genre}")
                        
                        if year:
                            return year, genre
            
            except Exception as e:
                continue
        
        return None, None
        
    except Exception as e:
        print(f"   ⚠️  AOTY search error: {e}")
        return None, None


def get_album_year(artist, album_name):
    """
    Get album year from multiple sources (Wikipedia, AOTY).
    
    Args:
        artist: Artist name
        album_name: Album name
        
    Returns:
        Year as integer or None if not found
    """
    # Try Wikipedia first
    print(f"   🔍 Searching Wikipedia...")
    year = search_wikipedia_album_year(artist, album_name)
    
    if year:
        return year
    
    # Try AOTY
    print(f"   🔍 Searching AOTY...")
    year, genre = search_aoty_album_info(artist, album_name)
    
    if year:
        return year
    
    print(f"   ❌ Could not find a valid year")
    return None


def folder_already_has_year(folder_name):
    """
    Check if folder name already has a year in parentheses.
    
    Args:
        folder_name: Name of the folder
        
    Returns:
        True if folder already has year, False otherwise
    """
    # Check for pattern like " (2012)" or " (1999)"
    pattern = r'\s*\(19\d{2}|20\d{2}\)\s*$'
    return bool(re.search(pattern, folder_name))


def add_year_to_folder_name(folder_path, year):
    """
    Rename folder to include the year in parentheses.
    
    Args:
        folder_path: Path to the folder
        year: Year to add
        
    Returns:
        New folder path or None if failed
    """
    try:
        parent_dir = os.path.dirname(folder_path)
        folder_name = os.path.basename(folder_path)
        
        # Check if already has year
        if folder_already_has_year(folder_name):
            print(f"   ℹ️  Folder already has a year")
            return folder_path
        
        # Create new folder name
        new_folder_name = f"{folder_name} ({year})"
        new_folder_path = os.path.join(parent_dir, new_folder_name)
        
        # Check if new folder already exists
        if os.path.exists(new_folder_path):
            print(f"   ⚠️  Folder with year already exists: {new_folder_name}")
            return folder_path
        
        # Rename folder
        os.rename(folder_path, new_folder_path)
        print(f"   ✅ Renamed to: {new_folder_name}")
        
        return new_folder_path
        
    except Exception as e:
        print(f"   ❌ Error renaming folder: {e}")
        return None


def process_album_folders(output_folder):
    """
    Process all album folders in the output directory and add year to folder names.
    
    Args:
        output_folder: Path to the output directory containing album folders
    """
    print(f"🔍 Scanning album folders in: {output_folder}\n")
    
    if not os.path.exists(output_folder):
        print(f"❌ Error: Output folder does not exist: {output_folder}")
        return
    
    # Get all subdirectories (album folders)
    album_folders = []
    for item in os.listdir(output_folder):
        item_path = os.path.join(output_folder, item)
        if os.path.isdir(item_path):
            album_folders.append(item_path)
    
    if not album_folders:
        print("ℹ️  No album folders found.")
        return
    
    print(f"📁 Found {len(album_folders)} album folder(s)\n")
    
    # Process each album folder
    for folder_path in album_folders:
        folder_name = os.path.basename(folder_path)
        print(f"📂 Processing: {folder_name}")
        
        # Skip if already has year
        if folder_already_has_year(folder_name):
            print(f"   ⏭️  Already has year, skipping...\n")
            continue
        
        # Get artist and album name from MP3 tags
        artist, album_name = get_album_info_from_tags(folder_path)
        
        if not artist or not album_name:
            print(f"   ⚠️  Could not get album info from tags, skipping...\n")
            continue
        
        print(f"   🎤 Artist: {artist}")
        print(f"   💿 Album: {album_name}")
        
        # Get album year from internet
        year = get_album_year(artist, album_name)
        
        if year:
            # Add year to folder name
            add_year_to_folder_name(folder_path, year)
        
        print()  # Empty line for readability
        time.sleep(1)  # Be respectful to websites
    
    print("✅ Processing complete!")


if __name__ == "__main__":
    # Check if argument is provided
    if len(sys.argv) < 2:
        print("Usage: python add_album_year.py <output_folder>")
        sys.exit(1)
    
    output_folder = sys.argv[1]
    
    # Validate that output folder exists
    if not os.path.exists(output_folder):
        print(f"❌ Error: Output folder does not exist: {output_folder}")
        sys.exit(1)
    
    # Process the album folders
    process_album_folders(output_folder)
