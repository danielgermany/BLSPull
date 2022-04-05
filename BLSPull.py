from selenium import webdriver
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

def getTitleGoogleSheet():
    gc = gspread.service_account(filename='file.json')
    sh = gc.open('Data Pull BLS')
    worksheet = sh.worksheet("Form Responses 3")
    list_of_title = worksheet.get_all_values()
    return list_of_title[-1][1]

def compareName(title):
    gc = gspread.service_account(filename='file.json')
    sh = gc.open('Data Pull BLS')
    worksheet = sh.worksheet("Refrence")
    lists_of_links = worksheet.get_all_values()
    for x in lists_of_links:
        if x[0] == title:
            return x[1]

def readFile(path):
    with open(path,"r") as f:
        SMRF1 = f.readlines()
    return SMRF1

def checkFileMod():
    initial = readFile()
    while True:
        current = readFile()
        if initial != current:
            for line in f:
                pass
            lastLink = line

            return True
            "Run the entire code here"

#pushtoGoogleSheet()
link = "https://www.bls.gov/oes/current/oes_ny.htm#31-00000"
name = "State Occupational Employment and Wage Estimates New York"


#name = getTitleGoogleSheet()
#link = compareName(name)

pushtoGoogleSheet(link,name)





























"""
counter = 0
for x in list_of_attributes:
    counter+=1
    print("This is iteration", counter)
    try:
        pushtoGoogleSheet(x,name + str(counter))
    except TypeError:
        print("Failed on iteration",counter)
        print(x)
"""

"""
dataFrame = pullBLS("https://data.bls.gov/projections/nationalMatrix?queryParams=621600&ioType=i")
row,col = dataFrame.shape
print(row)
"""
