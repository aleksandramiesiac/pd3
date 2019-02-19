"""
Wypisuje link do pobrania .7z każdego z forów
"""

from requests_html import HTMLSession

session = HTMLSession()
page = session.get("https://archive.org/download/stackexchange")

prefix = "https://archive.org/download/stackexchange/"
file_names = page.html.find("table[class=directory-listing-table] a[href$='7z']")[0:]

with open("linki.txt", "w") as f:
    for name in file_names:
        print(prefix+name.text, file=f)
