
# 📸 Flickr Album Downloader

This repository includes two Python scripts that allow you to **download entire albums from a Flickr user account** using the Flickr API.

---

## 🗂 Contents

- `flickr_album_downloader.py`  
  Basic version that downloads all photos from each album listed in a `flickr_albums.txt` file.

- `flickr_album_downloader_resume.py`  
  Enhanced version that supports **resuming** downloads if the process is interrupted (e.g., due to internet loss or system shutdown).

---

## 🧰 Requirements

Before running the scripts, install the required dependency:

```bash
pip install requests
```

---

## 🔧 Setup Instructions

1. **Get a Flickr API Key**  
   Sign up at: [https://www.flickr.com/services/api/misc.api_keys.html](https://www.flickr.com/services/api/misc.api_keys.html)

2. **Edit the Script**
   - Open either script in a code editor.
   - Replace the placeholder:
     ```python
     API_KEY = 'YOUR_API_KEY'
     ```
     with your actual Flickr API key.
   - `USER_ID`.

3. **Prepare Your Album List File**  
   Place `flickr_albums.txt` in the same folder as the script.  
   It should contain entries like:
   ```
   Album Title | Album Description | Photos: 45
   ```

---

## ▶️ Usage

Run the script from your terminal:

```bash
python flickr_album_downloader.py
# or
python flickr_album_downloader_resume.py
```

All images will be downloaded into folders under:
```
./flickr_downloads/
```

Each album will be saved to a folder named after its title. Images are named using a numbered prefix and the original photo title.

---

## 🔄 Version Comparison

| Feature                     | `flickr_album_downloader.py` | `flickr_album_downloader_resume.py` |
|----------------------------|------------------------------|-------------------------------------|
| Basic downloading          | ✅                            | ✅                                   |
| Resume support             | ❌                            | ✅                                   |
| Skips existing photo files | ❌                            | ✅                                   |
| Skips already completed albums | ❌                      | ✅                                   |
| Requires API key           | ✅                            | ✅                                   |

---

## ⚠️ Notes

- Avoid changing album titles in `flickr_albums.txt` after initial run if you plan to use resume.
- API rate limits apply — long pauses or high volume may need sleep intervals or retries.
- Ensure your internet connection is stable during long runs (or use the resume version).
