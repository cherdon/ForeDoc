import os
import json
from bs4 import BeautifulSoup


doc_toc_location = os.path.join(os.path.dirname(__file__), "docdata", "toc.json")
mod_toc_location = os.path.join(os.path.dirname(__file__), "docdata", "modules_toc.json")
final_search_file = os.path.join(os.path.dirname(__file__), "docdata", "index_new.json")

links = []
titles = []
unwanted_tags = [
    "[document]",
    "html",
    "script",
    "head",
    "label",
    "option",
    "form"
]
common_text = ["BeginSwitchLink", "EndSwitchLink"]


def expand(location):
    if location['children']:
        add(location)
        for header in location['children']:
            expand(header)
    else:
        add(location)


def add(location):
    links.append(location['link'])
    titles.append(location['title'])


def sanity_check(titles, links):
    if len(titles) == len(links):
        print("The compiler is completed, with no errors")
    else:
        print("Compiler has completed, but there are length mismatches")


if __name__ == "__main__":
    # with open(doc_toc_location, 'r') as f:
    #     doc = json.load(f)
    #
    # expand(doc)
    # sanity_check(titles, links)

    with open("templates/D_ProceduralBuildingOSM.html", "r") as f:
        contents = f.read()
    soup = BeautifulSoup(contents, 'html.parser')
    content = soup.find("div", {"class": "section"})
    text = content.find_all(text=True)
    # print(set([t.parent.name for t in text]))
    filtered_text = [t for t in text if t.parent.name not in unwanted_tags and t != "\n" and t not in common_text]
    for t in filtered_text[5:]:
        print("Format: {}\n Text: {}".format(t.parent.name, t))

