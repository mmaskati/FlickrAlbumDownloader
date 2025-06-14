import requests
import csv

API_KEY = #add API Key
USER_ID =  #add user ID
PER_PAGE = 100

albums = []
page = 1

while True:
	url = f'https://www.flickr.com/services/rest/?method=flickr.photosets.getList&api_key={API_KEY}&user_id={USER_ID}&format=json&nojsoncallback=1&per_page={PER_PAGE}&page={page}'
	response = requests.get(url)
	data = response.json()

	photosets = data['photosets']['photoset']
	if not photosets:
		break

	for album in photosets:
		title = album['title']['_content'].strip()
		desc = album['description']['_content'].strip()
		photo_count = album['photos']
		albums.append(f"{title} | {desc} | Photos: {photo_count}")

	print(f"Fetched page {page} with {len(photosets)} albums")
	page += 1

	if page > data['photosets']['pages']:
		break

# Optional: Deduplicate based on title (if duplicates exist)
unique_albums = list(dict.fromkeys(albums))

# Save all albums to a file
with open("flickr_albums.txt", "w", encoding="utf-8") as f:
	for line in unique_albums:
		f.write(line + "\n")

print(f"✅ Saved {len(unique_albums)} albums to flickr_albums.txt")
