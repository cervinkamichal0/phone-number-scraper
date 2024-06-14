import pycurl
import io
import gzip
from bs4 import BeautifulSoup
import re



def getPhoneNumber(Referer, idi, idPhone):
    response = io.BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://auto.bazos.cz/ad-phone.php')
    c.setopt(c.POST, 1)
    c.setopt(c.WRITEFUNCTION, response.write)

    c.setopt(c.POSTFIELDS, 'idi=187022655&idphone=23097')
    c.setopt(c.HTTPHEADER, ['Accept: /',
                            'Accept-Encoding: gzip, deflate, br, zstd',
                            'Accept-Language: cs-CZ,cz;q=0.9',
                            'Content-Length: 27',
                            'Content-Type: application/x-www-form-urlencoded',
                            'Cookie: rekkk=ano; _ga=GA1.1.1972335060.1717156671; cookie_consent_user_consent_token=IaxPN1F3GDNf; cookie_consent_user_accepted=true; bid=72447669; bkod=WY7UJ4RY43; testcookie=ano; cookie_consent_level=%7B%22strictly-necessary%22%3Atrue%2C%22functionality%22%3Atrue%2C%22tracking%22%3Atrue%2C%22targeting%22%3Atrue%7D; _ga_NZW1QTHKBB=GS1.1.1718355552.5.1.1718363569.0.0.0',
                            'Origin: https://auto.bazos.cz',
                            'Priority: u=1,i',
                            'Referer: https://auto.bazos.cz/inzerat/187022655/mazda-3-16-mz-cd-80-kw-klima-cr-nova-stk.php' ,
                            'Sec-Fetch-Dest: empty',
                            'Sec-Fetch-Mode: cors',
                            'Sec-Fetch-Site: same-origin',
                            'User-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'])
    c.perform()
    c.close()

    compressed_data = response.getvalue()
    response.close()

    # Dekompresování dat
    decompressed_data = gzip.decompress(compressed_data)
    return decompressed_data.decode('utf-8')

#getPhoneNumber('https://auto.bazos.cz/inzerat/187008051/skoda-fabia-3-fc-10tsi-70kw-combi-cr-dph-style-sport.php')

def getListingsUrls(pageNumber):
    response = io.BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://auto.bazos.cz/' + pageNumber)
    c.setopt(c.WRITEFUNCTION, response.write)
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
counter = 0
for listing in Listings:
    print(counter)
    print(listing)
    print(ids[counter][0])
    print(ids[counter][1])  
    print(getPhoneNumber(listing, ids[counter][0], ids[counter][1]))
    counter += 1