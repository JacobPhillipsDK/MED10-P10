import os
import requests

def download_tile(zoom, x, y):
    url = f"https://tile.openstreetmap.org/{zoom}/{x}/{y}.png"
    headers = {
        'Host': 'tile.openstreetmap.org',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,da;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Alt-Used': 'tile.openstreetmap.org',
        'Connection': 'keep-alive',
        'Cookie': '_osm_totp_token=876930',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-GPC': '1',
        'If-None-Match': '0e3be414c2f4a2d269f7b3940532c2e0'
    }
    response = requests.get(url, headers=headers)

    # Remove 'https://' from the URL before saving it as a file name
    file_path = os.path.join(os.getcwd(), f'{url.replace("https://", "").replace("/", "_")}.png')

    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download tile: {zoom}/{x}/{y}")

# Usage
download_tile(14, 8722, 5373)