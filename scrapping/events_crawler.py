import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib

def parse_location(location_string):
    matches = re.search(r'Ort: (.*)$', location_string.strip())

    if matches:
        return matches[1]
    else:
        return ""

def parse_date(date_string):
    matches = re.search(r'([0-9]{2})\.([0-9]{2})\.(2[0-9]{3})', date_string)
    year = matches[3]
    month = matches[2]
    day = matches[1]

    return datetime(int(year), int(month), int(day))


def get_latest_events():
    url = "https://www.fh-kufstein.ac.at/ger/Veranstaltungen"
    response = requests.get(url)

    input_html = BeautifulSoup(response.text, "html.parser")
    event_items = input_html.select('.news-item')

    event_list = []
    for event_item in event_items:
        title = event_item.select_one(".title").contents[0].strip()
        link_tag = event_item.select_one("a")
        full_date_container = event_item.select_one(".date")
        date = parse_date(full_date_container.contents[0].strip())
        location = parse_location(full_date_container.contents[2])
        description = event_item.select_one(".eztext-field")
        
        hash = hashlib.sha256()
        hash.update(bytes(title, 'utf-8'))
        hash.update(bytes(location, 'utf-8'))
        hash.update(bytes(str(date.time()), 'utf-8'))

        event_list.append({
            "name": title,
            "date": date,
            "location": location,
            "link": "http://www.fh-kufstein.ac.at" + link_tag["href"],
            "short": description.contents[0].strip(),
            "source": "FH Kufstein Homepage",
            "identifier": hash.hexdigest()
        })

    return event_list