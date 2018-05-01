

## 데이터를 csv로 저장

import csv

csvFile = open("test.csv", 'w+')
try:
    writer = csv.writer(csvFile)
    writer.writerow(('number', 'number plus 2', 'number times 2'))
    for i in range(10):
        writer.writerow((i, i+2, i*2))

finally:
    csvFile.close()


## 데이터를 csv로 저장

import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://en.wikipedia.org/wiki/Comparison_of_text_editors")
bsObj = BeautifulSoup(html, "html.parser")

table = bsObj.find_all("table", {"class": "wikitable"})[0]
rows = table.find_all("tr")
csvFile = open("editors.csv", "wt")
writer = csv.writer(csvFile)

try:
    for row in rows:
        csvRow = []
        for cell in row.find_all(['td', 'th']):
            csvRow.append(cell.get_text().encode('utf-8'))
        writer.writerow(csvRow)
finally:
    csvFile.close()

