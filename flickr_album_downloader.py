
import os
import re
import requests
import time

API_KEY = 'API Key'  # Replace with your actual Flickr API key
USER_ID = 'USER ID'

# Load albums from flickr_albums.txt
with open('flickr_albums.txt', 'r', encoding='utf-8') as file:
    album_lines = [line.strip() for line in file if line.strip()]

# Regex pattern to split album title and photo count
album_pattern = re.compile(r'^(.*?)\s*\|\s*.*?\|\s*Photos:\s*(\d+)$')

# Create base directory for downloads
base_download_path = 'flickr_downloads'
os.makedirs(base_download_path, exist_ok=True)

# Fetch all albums from API (in memory, match by title)
def get_all_albums():
    albums = []
    page = 1
    while True:
        url = f'https://www.flickr.com/services/rest/?method=flickr.photosets.getList&api_key={API_KEY}&user_id={USER_ID}&format=json&nojsoncallback=1&per_page=100&page={page}'
        response = requests.get(url)
        data = response.json()
        photosets = data.get('photosets', {}).get('photoset', [])
        if not photosets:
            break
        for ps in photosets:
            albums.append({
                'id': ps['id'],
                'title': ps['title']['_content'].strip().replace('/', '-')
            })
        if page >= data['photosets']['pages']:
            break
        page += 1
    return albums

all_albums_api = get_all_albums()

# Process each line from text file
for line in album_lines:
    match = album_pattern.match(line)
    if not match:
        continue
    album_title, photo_count = match.groups()
    album_title_clean = album_title.strip().replace('/', '-')

    # Find album ID by matching title
    album_info = next((a for a in all_albums_api if a['title'] == album_title_clean), None)
    if not album_info:
        print(f"❌ Album not found on API: {album_title_clean}")
        continue

    album_id = album_info['id']
    folder_path = os.path.join(base_download_path, album_title_clean)
    os.makedirs(folder_path, exist_ok=True)

    # Fetch photos in album
    photo_url = f'https://www.flickr.com/services/rest/?method=flickr.photosets.getPhotos&api_key={API_KEY}&photoset_id={album_id}&user_id={USER_ID}&format=json&nojsoncallback=1&per_page=500'
    photo_response = requests.get(photo_url)
    photo_data = photo_response.json()
    photos = photo_data.get('photoset', {}).get('photo', [])

    print(f"📂 Downloading {len(photos)} photos from: {album_title_clean}")

    for i, photo in enumerate(photos):
        photo_id = photo['id']
        photo_title = photo['title'].strip().replace('/', '-')
        size_url = f'https://www.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key={API_KEY}&photo_id={photo_id}&format=json&nojsoncallback=1'
        size_response = requests.get(size_url)
        size_data = size_response.json()
        sizes = size_data.get('sizes', {}).get('size', [])
        if not sizes:
            print(f"⚠️ No sizes found for photo {photo_id}")
            continue
        image_url = sizes[-1]['source']
        image_data = requests.get(image_url)
        if image_data.status_code == 200:
            image_path = os.path.join(folder_path, f"{i+1:03d}_{photo_title}.jpg")
            with open(image_path, 'wb') as img_file:
                img_file.write(image_data.content)
            print(f"✅ {album_title_clean}: Saved {photo_title}")
        else:
            print(f"❌ Failed to download photo: {photo_title}")
        time.sleep(1)  # Wait between downloads
    print(f"✅ Completed: {album_title_clean}\n")
