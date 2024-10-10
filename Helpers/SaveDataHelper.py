import json

from pydantic import BaseModel
from MSSQLHelper import MSSqlHelper


class ApiRequestModel(BaseModel):
    id: int
    sglUniqueModelCode: str
    section: str
    partNumber: str
    description: str
    itemNumber: str
    sectonDiagram: str
    sectonDiagramUrl: str
    scraperName: str


def _create_records(items) -> list[dict]:
    records = []
    for item in items:
        sgl = item['SGL']
        section = item['Catalog']
        img_url = item['Img Url']
        img_filename = item['Img Filename']
        parts = item['Parts']
        for part in parts:
            records.append(ApiRequestModel(
                id=0,
                sglUniqueModelCode=sgl,
                section=section,
                partNumber=part['Item Number'],
                description=part['Desctiption'],
                itemNumber='',
                sectonDiagram=img_filename,
                sectonDiagramUrl=img_url,
                scraperName='Al-Ko').model_dump())
    return records


with open(r'D:\Workspace\Projects\AlKoScraper\Translated Data.json', 'r') as scraped_data_file:
    scraped_data = json.loads(scraped_data_file.read())
records = _create_records(scraped_data)
MSSqlHelper().insert_many_records(records)
