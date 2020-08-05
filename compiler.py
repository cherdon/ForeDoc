import os
import json
from bs4 import BeautifulSoup
import string
import re


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


def parse_word(word):
    parsed = word.lower()
    parsed = parsed.strip(" ")
    parsed = re.sub("\n", "", parsed)
    parsed = parsed.strip(string.punctuation)
    parsed = parsed.strip(" ")
    return parsed


if __name__ == "__main__":
    index_json = {}
    index_json['common'] = {"the":1,"you":1,"a":1,"both":1,"that":1,"not":1,"print":1,"see":1,"if":1,"on":1,"or":1,"in":1,"this":1,"also":1,"only":1,"returns":1,"ref":1,"for":1,"by":1,"be":1,"used":1,"wiki":1,"class":1,"with":1,"and":1,"none":1,"function":1,"of":1,"are":1,"attached":1,"is":1,"to":1,"use":1,"will":1,"from":1,"var":1,"at":1,"get":1,"set":1,"when":1,"it":1,"can":1,"as":1,"an":1}

    # Reading all HTML files
    with open(doc_toc_location, 'r') as f:
        doc = json.load(f)

    expand(doc)
    sanity_check(titles, links)
    print(titles)
    print(links)

    # ADD PAGES
    index_json['pages'] = list()
    index_json['info'] = list()
    index_json['searchIndex'] = dict()
    for i in range(len(titles)):
        if i == 0:
            pass
        else:
            print("Parsing through {}/{} links".format(str(i), str(len(titles))))
            index_json['pages'].append([links[i], titles[i].strip(" ")])

            # Opening individual HTML files
            with open("templates/{}.html".format(links[i]), "r") as f:
                contents = f.read()
            soup = BeautifulSoup(contents, 'html.parser')
            content = soup.find("div", {"class": "section"})
            text = content.find_all(text=True)
            filtered_text = [t for t in text if t.parent.name not in unwanted_tags and t != "\n" and t not in common_text]
            for t in filtered_text[5:-2]:
                sentence = parse_word(t)
                if sentence != "":
                    index_json['info'].append([sentence, i])

                words = [parse_word(word) for word in t.split(" ") if word != ""]
                for word in words:
                    if word not in index_json['common'].keys():
                        if word in index_json['searchIndex']:
                            index_json['searchIndex'][word].append(i)
                        else:
                            index_json['searchIndex'][word] = [i]
                # print("Format: {}\n Text: {}".format(t.parent.name, t))

    # Unique search index
    index_json['searchIndex'] = {key: list(set(value)) for key, value in index_json['searchIndex'].items()}

    print(index_json['info'])
    print(len(index_json['searchIndex']))

    # Storing final file
    with open(final_search_file, 'w') as fp:
        json.dump(index_json, fp)

