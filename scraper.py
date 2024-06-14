import pycurl
import io

response = io.StringIO()
c = pycurl.Curl()
c.setopt(c.URL, 'https://auto.bazos.cz/ad-phone.php')
c.setopt(pycurl.POST, 1)
c.setopt(c.WRITEFUNCTION, response.write)
c.setopt(pycurl.COOKIEJAR, 'cookie.txt')
c.setopt(pycurl.COOKIEFILE, 'cookie.txt')
c.setopt(c.HTTPHEADER, ['Accept: /',
                        'Accept-Encoding: gzip, deflate, br',
                        'Accept-Language: cs-CZ,cz;q=0.9',
                        'Content-Length: 29',
                        'Content-Type: application/x-www-form-urlencoded',
                        'Origin: https://auto.bazos.cz',
                        'Priority/: u=1,i' ,
                        'Referer: https://auto.bazos.cz/inzerat/186600399/mercedes-benz-c63-amg-w204.php',
                        'Sec-Fetch-Dest: empty', 'Sec-Fetch-Mode: cors',
                        'Sec-Fetch-Site: same-origin',
                        'User-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'])
c.perform()
c.close()
print(response.getvalue())
response.close()