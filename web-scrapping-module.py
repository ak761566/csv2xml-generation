from pprint import pprint

import requests
from bs4 import BeautifulSoup
import re
URL = "http://idrive.portico.org/pcontent/ongoing/journal_content/INGEST_MASTER/_dcollections/AMDIGITAL/Fetched/CHINA_ON_FILM/NEW/Assets/Transcripts/WebVTT/"

OUTPUT_LOCATION = "/Portico-Project/Amdigital/CHINA_ON_FILM/China_On_File_Python_Script_ref.csv"

response = requests.get(URL)
i_drive_web_page = response.text
#print(response.text)

soup = BeautifulSoup(i_drive_web_page, "html.parser")
data = soup.body.table
# print(data.find_all(href=re.compile(".*\\.[a-z0-9]{2,4}")))

all_anchor_tag = data.find_all(href=re.compile(".*\\.[a-z0-9]{2,4}"))

with open(OUTPUT_LOCATION, "a+") as out_file:
    for tag in all_anchor_tag:
        out_data = f"{tag.get('href').split('.')[0]},{tag.get('href')}\n"
        out_file.write(out_data)


















# with open("portico-i-drive-source-data.html") as file:
#     content = file.read()
#
# soup = BeautifulSoup(content, "html.parser")
# # print(soup.html.body.table)
#
# all_anchor_tag = soup.find_all("a")
# # print(all_anchor_tag)
#
# all_anchor = soup.select(selector="tr td a")
# # print(all_anchor)
#
# # for anchor in all_anchor:
# #     print(anchor.get("href"))
