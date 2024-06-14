import pycurl
import io

response = io.BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, 'https://auto.bazos.cz/ad-phone.php')
c.setopt(c.POST, 1)
c.setopt(c.WRITEFUNCTION, response.write)
c.setopt(c.COOKIEJAR, 'token.txt')
c.setopt(c.COOKIEFILE, 'token.txt')
c.setopt(c.POSTFIELDS, 'idi=187008051&idphone=4897862')
c.setopt(c.HTTPHEADER, ['Accept: /',
                        'Accept-Encoding: gzip, deflate, br, zstd',
                        'Accept-Language: cs-CZ,cz;q=0.9',
                        'Content-Length: 29',
                        'Content-Type: application/x-www-form-urlencoded',
                        'Origin: https://auto.bazos.cz',
                        'Priority: u=1,i',
                        'Referer: https://auto.bazos.cz/inzerat/187008051/skoda-fabia-3-fc-10tsi-70kw-combi-cr-dph-style-sport.php',
                        'Sec-Fetch-Dest: empty',
                        'Sec-Fetch-Mode: cors',
                        'Sec-Fetch-Site: same-origin',
                        'User-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'])
c.perform()
c.close()

print(print(response.getvalue().decode('windows-1252')))
response.close()