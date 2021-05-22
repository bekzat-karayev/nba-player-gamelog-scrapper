
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas
import re
import shutil
import os
import glob

def GeneratePlayerLinks():
    player_links = []
    pattern = re.compile(r"\\\w*,")

    with open ('playerstatscsv.txt') as myfile:
        for myline in myfile:
            if pattern.search(myline) != None:
                found = re.search(pattern, myline).group(0)
                found = found.replace('\\', '').replace(',','')
                player_links.append(found)

    return player_links

def WritePlayerLinksToFile():
    names = GeneratePlayerLinks()
    names = list(dict.fromkeys(names))

    f = open("playerlinks.txt", "w+")

    for name in names:
        f.write("/" + name[0] + "/" + name + "\n")

    f.close()

def ScrapeGameLogs(): 
    #ExtractPlayerLinks()
    year = "/gamelog/2021"
    f = open("playerlinks.txt", "r").readlines()

    player_links = []

    for link in f:
        player_links.append(link)

    for link in player_links:
        url = "https://www.basketball-reference.com/players%s%s" % (link.strip('\n'), year)

        html = urlopen(url)

        soup = BeautifulSoup(html, features="html.parser")

        tag = soup.find('h1', itemprop="name")
        title = tag.text.split(' ')
        name = "{0}, {1}".format(title[1], title[0].lstrip('\n'))

        headers = [th.getText() for th in soup.find('thead').findAll('th')]

        headers = headers[1:]
        rows = soup.find('table', id="pgl_basic").find_all('tr')[1:]
        games = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

        gamelog = pandas.DataFrame(games, columns = headers)

        with pandas.ExcelWriter('players/{0}.xlsx'.format(name)) as writer:
            gamelog.to_excel(writer, sheet_name='{0}'.format(name))

        print(name)

ScrapeGameLogs()