import re
import requests
from bs4 import BeautifulSoup

OUT_FILE = "stdb.txt"
URL = "https://www.gesetze-im-internet.de/englisch_stgb/"

pattern = re.compile("(?P<section>Section)\\s(?P<number>\\d*[a-z]?)(?P<text>(.+))")


def get_body(url: str) -> requests.request:
    r = requests.get(url)
    if r.status_code == 200:
        return r


def parse_body(r: requests.request):
    lines = []
    soup = BeautifulSoup(r.text, "html.parser")

    for i in soup.find_all("tr"):
        tr_text = i.get_text()
        if "Section" in tr_text:
            x = pattern.match(tr_text)
            if x is not None:
                lines.append(
                    f"{x['section']} {x['number']} German Criminal Code - {x['text']}"
                )

    return lines


def main():
    r = get_body(URL)
    lines = parse_body(r)

    with open(OUT_FILE, "w") as file:
        for line in lines:
            file.write(f"{line}\n")


if __name__ == "__main__":
    main()
