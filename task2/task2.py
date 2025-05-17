import logging
from collections import defaultdict
from pathlib import Path

import requests
from bs4 import BeautifulSoup


URL = (
    "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту"
)

def request_page(pagefrom: str | None) -> (dict[str, int], str):
    """Gets a wikipedia page with animals, returns counts by starting letter & last name on the page

    Args:
        pagefrom: animal name to start the page with; if None, gets the first page; else doesn't count the first
            name to account for page intersections
    """

    url = (pagefrom is not None
        and f"{URL}&pagefrom={pagefrom.replace(' ', '+')}"
        or URL)
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    counters = {}
    last = None

    content_parent = soup.find(lambda tag: tag.h2 and "Страницы в категории" in tag.h2.text)
    is_first_iteration = True
    for group in content_parent.find_all("div", class_="mw-category-group"):
        letter = group.h3.text
        children = group.ul.find_all("a")

        counters[letter] = len(children)
        if is_first_iteration and pagefrom is not None:
            counters[letter] -= 1
        last = children[-1].text

        is_first_iteration = False

    return counters, last


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting")

    result = defaultdict(int)
    last = None

    while True:
        counters, new_last = request_page(last)

        if new_last == last:
            break

        last = new_last
        for k, v in counters.items():
            result[k] += v

        logging.info(f"{counters} {last}")
        # may want to change this message's log level for production

    logging.info("Fetched all data, writing beasts.csv")
    Path("beasts.csv").write_text("\n".join(f"{k},{v}" for k, v in result.items()), encoding='utf-8')
    logging.info("Done.")
