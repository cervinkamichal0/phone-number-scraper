import pycurl
import io
import gzip
from bs4 import BeautifulSoup
import re
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# Todel aby fungovalo jak v konteineru tak na localu
def set_cainfo(c):
    ca_path = '/etc/ssl/certs/ca-certificates.crt'
    if os.path.exists(ca_path):
        c.setopt(pycurl.CAINFO, ca_path)


def getPhoneNumber(Referer, idi, idPhone):
    response = io.BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://auto.bazos.cz/ad-phone.php')
    c.setopt(c.POST, 1)
    c.setopt(c.WRITEFUNCTION, response.write)

    c.setopt(c.POSTFIELDS, 'idi=' + idi + '&idphone=' + idPhone)
    c.setopt(c.HTTPHEADER, ['Accept: /',
                            'Accept-Encoding: gzip, deflate, br, zstd',
                            'Accept-Language: cs-CZ,cz;q=0.9',
                            'Content-Type: application/x-www-form-urlencoded',
                            'Cookie: rekkk=ano; _ga=GA1.1.646289452.1717752234; __gsas=ID=6189362fdc6b1e38:T=1717752240:RT=1717752240:S=ALNI_MbHd4SkLID6hlaAYwjxAwW4ExH_hA; cookie_consent_user_consent_token=ddymkzb5E7lF; cookie_consent_user_accepted=true; testcookie=ano; bid=72394779; btelefon=732111027; testcookieaaa=ano; rekkkb=ano; bkod=11XRGOUUOG; bmail=cervinkamichal0%40gmail.com; bjmeno=Michal; bheslo=Misa4589_; cookie_consent_level=%7B%22strictly-necessary%22%3Atrue%2C%22functionality%22%3Atrue%2C%22tracking%22%3Atrue%2C%22targeting%22%3Atrue%7D; _ga_NZW1QTHKBB=GS1.1.1718394476.11.1.1718394480.0.0.0',
                            'Origin: https://auto.bazos.cz',
                            'Priority: u=1,i',
                            'Referer: ' + Referer,
                            'Sec-Fetch-Dest: empty',
                            'Sec-Fetch-Mode: cors',
                            'Sec-Fetch-Site: same-origin',
                            'User-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'])
    set_cainfo(c)
    c.perform()
    c.close()

    compressed_data = response.getvalue()
    response.close()

    # Decompress data
    decompressed_data = gzip.decompress(compressed_data)
    return decompressed_data

def getListingsUrls(pageNumber):
    response = io.BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://auto.bazos.cz/' + pageNumber)
    c.setopt(c.WRITEFUNCTION, response.write)
    set_cainfo(c)
    c.perform()
    c.close()

    decodedResponse = response.getvalue().decode('utf-8')

    soup = BeautifulSoup(decodedResponse, 'html.parser')
    divs = soup.find_all('div', class_='inzeraty inzeratyflex')
    hrefs = []
    for div in divs:
        hrefs.append(div.find('a')['href'])
    for href in hrefs:
        hrefs[hrefs.index(href)] = 'https://auto.bazos.cz' + href
    return hrefs

def getIdsFromListings(listings):
    ids=[]
    for url in listings:
        response = io.BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEFUNCTION, response.write)
        set_cainfo(c)
        c.perform()
        c.close()

        decodedResponse = response.getvalue().decode('utf-8')

        soup = BeautifulSoup(decodedResponse, 'html.parser')
        span = soup.find('span', class_='teldetail')
        onclick_value = span.get('onclick')
        id = re.findall(r'\d{3,}', onclick_value)
        ids.append(id)
    return ids

Listings = getListingsUrls('20')
ids = getIdsFromListings(Listings)

# Set up access rights and authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope) #json file will not be uploaded to GitHub
client = gspread.authorize(creds)

# Create a Google Sheet instance (link to the sheet in commit message)
sheet = client.open("BazosPhones").sheet1

counter = 0
for listing in Listings:
    if counter % 3 == 0 and counter != 0:
        time.sleep(20)
    print(counter)
    print(listing)
    print(ids[counter][0])
    print(ids[counter][1])
    row = getPhoneNumber(listing, ids[counter][0], ids[counter][1])  
    print(row)

    # Write to Google Sheet
    sheet.append_row([str(row)])
    counter += 1
