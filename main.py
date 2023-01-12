import requests as r
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime as dt

JSON_PATH = "genstats.json"

stats_file = open(JSON_PATH, "r")
existing_data = []
try:
    existing_data = json.load(stats_file)
except:
    existing_data = []
req = r.get("https://www.zpc.co.zw/")
html = req.text
soup = bs(html, 'html.parser')
stations = soup.find_all(class_="station")
outputs = soup.find_all(class_="output")
date = soup.find(class_="date").string.lstrip("Last Updated: ")
date = dt.strptime(date, "%d %B %Y").isoformat()
new_data = {
    "fetched": dt.now().isoformat(),
    "last_updated": date
}
if len(stations) == len(outputs):
    for station, output in zip(stations, outputs):
        sname = station.string.strip().title()
        ogen = output.string.strip()
        ogen = int(output.string.rstrip("MW"))
        new_data[sname] = ogen
existing_data.append(new_data)
stats_file.close()
stats_file = open(JSON_PATH, "w")
json.dump(existing_data, stats_file, indent=4)
stats_file.close()
