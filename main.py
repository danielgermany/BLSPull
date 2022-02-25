from selenium import webdriver
from bs4 import BeautifulSoup

import pandas as pd
import gspread
from df2gspread import df2gspread as d2g

def pullBLS(url):
    #request_json = request.get_json()
    #htmlID = 'mytable'

    data = []
    list_header = []
    elements = []
    attribute = []

    driver = webdriver.Chrome(executable_path=".\chromedriver.exe")
    driver.get(url)
    #.get_attribute('outerHTML')
    html = driver.find_element_by_id('DataTables_Table_0' or 'oes')

    print("Closing driver")

    driver.quit()

    return html

def makeDataFrame(i):
    print("starting to make data frame")
    soup = BeautifulSoup(i,'html.parser')
    header = soup.find_all("table")[0].find("tr")

    for items in header:
        try:
            list_header.append(items.get_text())
        except:
            continue

    HTML_data = soup.find_all("table")[0].find_all("tr")[1:]

    for element in HTML_data:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text())
            except:
                continue
        data.append(sub_data)

    dataFrame = pd.DataFrame(data = data, columns = list_header)

    return dataFrame

def pushtoGoogleSheet(link,name):
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



#pushtoGoogleSheet()
name = getTitleGoogleSheet()
link = compareName(name)
list_of_attributes = pullBLS(link)

pushtoGoogleSheet(list_of_attributes,name)
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
