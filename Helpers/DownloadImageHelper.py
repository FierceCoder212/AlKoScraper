import json

import requests
from PIL import Image
from io import BytesIO

with open(r'D:\Workspace\Projects\AlKoScraper\Translated Data.json', 'r') as json_file:
    data = [{"Img Url": item["Img Url"], 'Img Filename': item['Img Filename']} for item in json.load(json_file)]
for d in data:
    img_url = d["Img Url"]
    img_filename = d["Img Filename"]
    response = requests.get(img_url)
    if response.status_code == 200:
        # Open the image using PIL
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")
        # Save the image in PNG format to avoid compatibility issues
        img.save(fr'D:\Workspace\Projects\AlKoScraper\Images\{img_filename}', "JPEG")
        print(f"Image downloaded and saved as '{img_filename}'")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
