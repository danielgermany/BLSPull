from bs4 import BeautifulSoup

import urllib.request as r

import pandas as pd
import gspread
from df2gspread import df2gspread as d2g

def pullBLS(url):
    page = r.urlopen(url)
    return page.read().decode('utf8')

def parseHTML(html):
    soup = BeautifulSoup(html)
    tables = soup.findAll("table")

    for table in tables:
        if table.findParent("table") is None:
            print(str(table))

def makeDataFrame(i):
    print("starting to make data frame")
    data = []

    # for getting the header from
    # the HTML file
    list_header = []
    soup = BeautifulSoup(i,'html.parser')
    header = soup.find_all("table")[0].find("tr")

    for items in header:
        try:
            list_header.append(items.get_text())
        except:
            continue

    # for getting the data
    HTML_data = soup.find_all("table")[0].find_all("tr")[1:]

    for element in HTML_data:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text())
            except:
                continue
        data.append(sub_data)
    print(list_header)
    # Storing the data into Pandas
    # DataFrame
    dataFrame = pd.DataFrame(data = data)
    return dataFrame

def pushtoGoogleSheet(link,name):
    iter = pullBLS(link)
    parseHTML(iter)
    df = makeDataFrame(iter)
    row,col = df.shape
    gc = gspread.service_account(filename='file.json')
    sh = gc.open('Data Pull BLS')

    worksheet = sh.add_worksheet(title=name,rows=row,cols=col)
    #worksheet = sh.worksheet("test")
    print("Sending to Spreadsheet...")
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print("Pushed to sheet")

def readFile(path):
    with open(path,"r") as f:
        SMRF1 = f.readlines()
    return SMRF1

def checkFileMod():
    print("Checking initial file...")
    initial = readFile("BLSlists.txt")
    while True:
        current = readFile("BLSlists.txt")
        if initial != current:
            print("Change detected...")
            for line in current:
                pass
            lastLink = line
            with open("BLSlists_name.txt") as l:
                for line in l:
                    pass
                lastname = line
            initial = current
            pushtoGoogleSheet(lastLink,lastname)






checkFileMod()
