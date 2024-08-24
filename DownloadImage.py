import json

import requests
from PIL import Image
from io import BytesIO

with open('Scraped Data.json', 'r') as json_file:
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
        img.save(f'Images/{img_filename}', "JPEG")
        print("Image downloaded and saved as 'downloaded_image.png'")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
