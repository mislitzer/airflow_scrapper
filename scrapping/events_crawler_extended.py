import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
import hashlib

def parse_date(date_string, current_year):
    matches = re.search(r'([0-9]{2})\.([0-9]{2})', date_string)
    month = matches[2]
    day = matches[1]

    return datetime(int(current_year), int(month), int(day))


def get_latest_events_extended():
    url = "https://www.dolomitenstadt.at/veranstaltungen/"
    response = requests.get(url)

    input_html = BeautifulSoup(response.text, "html.parser")
    event_items = input_html.select('.page__veranstaltungen__block')
    today_date = date.today()

    event_list = []
    for event_item in event_items:
        block_title = event_item.select_one(".page__veranstaltungen__block__title").contents[0].strip()
        block_contents = event_item.select_one(".page__veranstaltungen__block__content")

        for block_content in block_contents:
            title = event_item.select_one(".page__veranstaltungen__item__title").contents[0].strip()
            link_tag = event_item.select_one("a")
            full_date_container = event_item.select_one(".page__veranstaltungen__item__time").contents[0].strip()
            location = event_item.select_one(".page__veranstaltungen__item__location").contents[0].strip()
            date_insert = None

            # seperate date
            if (block_title == "Heute"):
                date_insert = today_date
            elif (block_title == "Morgen"):
                tommorow_date = today_date + timedelta(days=1)
                date_insert = tommorow_date
            else:
                date_insert = parse_date(full_date_container, today_date.year)

            hash = hashlib.sha256()
            hash.update(bytes(title, 'utf-8'))
            hash.update(bytes(location, 'utf-8'))
            hash.update(bytes(str(date_insert), 'utf-8'))

            event_list.append({
                "name": title,
                "date": date_insert,
                "location": location,
                "link": link_tag["href"],
                "short": "Dolomitenstadt.at - " + title,
                "source": "Dolomitenstadt Lienz",
                "identifier": hash.hexdigest()
            })

        return event_list