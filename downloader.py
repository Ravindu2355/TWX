import requests
import time
import os

def download_file(url, filename, progress_callback=None):
    """Download with progress callback"""
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        downloaded = 0
        start = time.time()
        last_update = start

        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    now = time.time()
                    if progress_callback and now - last_update >= 10:
                        percent = (downloaded / total * 100) if total else 0
                        progress_callback(downloaded, total, percent, now - start)
                        last_update = now

    return filename
