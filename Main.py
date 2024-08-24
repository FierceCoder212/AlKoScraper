import json

completed_codes = ['de', 'German_fi', 'uk', 'at', 'lt', 'ro', 'lv', 'ee', 'cz', 'it', 'dk', 'se', 'pl', 'no', 'hr',
                   'si', 'ch', ]


def remove_values(value, country_code):
    catalog = value['Catalog']
    remove = ['solo®', 'by', 'By', 'BY', 'Solo', 'Al-ko', 'AL-KO', 'AL-KO']
    for r in remove:
        catalog = catalog.replace(r, '')
    value['Catalog'] = ' '.join([item for item in str(catalog).rstrip('Al').rstrip('B').strip().split(' ') if item])
    if country_code == 'German_fi':
        country_code = 'en'
    value['lang'] = country_code
    return value


files_data = []
for completed_code in completed_codes:
    with open(f"{completed_code}.json", 'r') as json_file:
        files_data.extend([remove_values(d, completed_code) for d in json.load(json_file)])
with open(f"All Data.json", 'w') as json_file:
    json_file.write(json.dumps(files_data, indent=4))
