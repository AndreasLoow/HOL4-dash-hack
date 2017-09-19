#!/usr/bin/env python3

# Required packages: BeautifulSoup4 lxml

import shutil
import sqlite3
import sys
import os

from bs4 import BeautifulSoup

def scrape_index(path, ty):
    ret = []

    with open(path) as fp:
        tree = BeautifulSoup(fp, "lxml")

        for e in tree.find_all("li"):
            bs = e.find_all("b")
            assert(len(bs) == 1)

            for a in e.find_all("a"):
                ret.append((a.text + "." + bs[0].text, ty, a.get("href")))

    return ret


def copy_and_replace_str(src, dst, needle, repstr):
    with open(src) as fr:
        fc = fr.read()

    fc = fc.replace(needle, repstr)

    with open(dst, "w") as fw:
        fw.write(fc)

# Sanity check
cwd = os.path.realpath(os.getcwd())
dirname = os.path.basename(cwd)
if dirname != "help":
    print("You must run this script from the help directory in your HOL4 installation.")
    sys.exit(1)

print("Copying HTML files (1)...")
# Directory must not exists
shutil.copytree("Docfiles/HTML", "HOL4.docset/Contents/Resources/Documents/Docfiles")

print("Copying HTML files (2)...")
# Need to hack some links to "Docfiles"
#shutil.copytree("src-sml/htmlsigs/", "HOL4.docset/Contents/Resources/Documents")

basedelpath = "file://" + cwd
delpath = basedelpath + "/Docfiles/HTML/"

for f in os.listdir("src-sml/htmlsigs"):
    copy_and_replace_str(os.path.join("src-sml/htmlsigs", f),
                         os.path.join("HOL4.docset/Contents/Resources/Documents", f),
                         delpath,
                         "Docfiles/")

shutil.copy("Docfiles/doc.css", "HOL4.docset/Contents/Resources/Documents")

copy_and_replace_str("HOLindex.html", "HOL4.docset/Contents/Resources/Documents/index.html",
                     basedelpath + "/src-sml/htmlsigs/", "")

scriptdir = os.path.dirname(os.path.realpath(__file__))
shutil.copy(os.path.join(scriptdir, "Info.plist"), "HOL4.docset/Contents")

print("Building index...")
idx = []
idx.extend(scrape_index("src-sml/htmlsigs/idIndex.html", "Interface"))
idx.extend(scrape_index("src-sml/htmlsigs/TheoryIndex.html", "Environment"))

print("Creating database...")
conn = sqlite3.connect("HOL4.docset/Contents/Resources/docSet.dsidx")
c = conn.cursor()

c.execute("CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT)")
c.execute("CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path)")
conn.commit()

c.executemany("INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?, ?, ?)", idx)
conn.commit()

conn.close()
