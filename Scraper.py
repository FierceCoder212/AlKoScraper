import json
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def translate_data(data: list[str], lang):
    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/json+protobuf",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "x-client-data": "CIu2yQEIprbJAQipncoBCKeXywEIk6HLAQia/swBCOmYzQEIhaDNAQ==",
        "x-goog-api-key": "AIzaSyATBXajvzQLTDHEQbcpq0Ihe0vWDHmO520",
    }

    url = "https://translate-pa.googleapis.com/v1/translateHtml"
    body = [[data, lang, "en"], "te_lib"]
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        try:
            return json.loads(response.text)[0]
        except Exception as ex:
            print(f'Error at google translate : {ex}\n{response.text}')
    else:
        print(f'Error at translation, Status code : {response.status_code}')
    return data


def get_spare_parts(soup: BeautifulSoup):
    spare_parts = soup.select(
        'div[class="imagemap-content accordion"] input.search-for-spareparts+div.row div.table-rows')
    spare_part_obj = []
    for spare_part in spare_parts:
        items = [item for item in spare_part.text.split('\n') if item]
        item_number = items[0]
        description = items[1]
        spare_part_obj.append({
            'Item Number': item_number,
            'Description': description
        })
    return spare_part_obj


def _sanitize_filename(filename: str) -> str:
    invalid_chars = r'[<>:"/\\|?*\']'
    sanitized_filename = re.sub(invalid_chars, "_", filename)
    sanitized_filename = sanitized_filename.strip()
    sanitized_filename = sanitized_filename[:255]
    return sanitized_filename


def scrape_data(data):
    url = data['URL']
    catalog = data['Catalog']
    sgl_code = data['SGL']
    language = data['lang']
    try:
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            html = response.json()['html']
            soup = BeautifulSoup(html, 'html.parser')
            img_url = urljoin(url, soup.select_one('div.explodedViewsContainer img').get('src'))
            parts = get_spare_parts(soup)
            translated_parts = translate_data([part['Description'] for part in parts], language)
            for part, translated_description in zip(parts, translated_parts):
                part['Description'] = translated_description
            img_filename = _sanitize_filename(f'{sgl_code}-{catalog}.jpg')
            return {
                'SGL': sgl_code,
                'Catalog': catalog,
                'Parts': parts,
                'Img Url': img_url,
                'Img Filename': img_filename
            }
        else:
            print('Response Error')
    except Exception as e:
        print(f'Exception at {sgl_code}')
    return None


with open(f"All Data.json", 'r') as json_file:
    all_data = json.load(json_file)

objs = []
for index, d in enumerate(all_data):
    print(f'On {index} out of {len(all_data)} : {d['SGL']}')
    val = scrape_data(d)
    if val:
        objs.append(val)

with open(f"Scraped Data.json", 'w') as json_file:
    json_file.write(json.dumps(objs, indent=4))
