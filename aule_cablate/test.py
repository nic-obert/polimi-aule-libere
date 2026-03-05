import requests as r


FROM_DAY = "1"
FROM_MESE = "3" # Marzo
FROM_ANNO = "2025"
TO_DAY = "31"
TO_MESE = "3" # Marzo
TO_ANNO = "2025"

URL_BASE_AULE_CONTROLLER = "https://onlineservices.polimi.it/spazi/spazi/controller/"


ID_AULA = "75"


url = "https://onlineservices.polimi.it/spazi/spazi/controller/Aula.do?jaf_currentWFID=main"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.5",
    "Cache-Control": "max-age=0",
    "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarynkcqVmj0dR7WSFkv",
    "Origin": "https://onlineservices.polimi.it",
    "Priority": "u=0, i",
    "Referer": f"https://onlineservices.polimi.it/spazi/spazi/controller/Aula.do?evn_init=event&idaula={ID_AULA}&jaf_currentWFID=main",
    "Sec-CH-UA": '"Not:A-Brand";v="99", "Brave";v="145", "Chromium";v="145"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Linux"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Sec-GPC": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "Cookie": "INGRESSCOOKIE=1772650412.855.35713.987370|276e15ac331c317751f24d44a9aebc2c; JSESSIONID=aaaI8hNSVm_5sfE1-R3Yz"
}

# Raw multipart form-data body as string including boundary and CRLFs
multipart_body = f"""------WebKitFormBoundarynkcqVmj0dR7WSFkv
Content-Disposition: form-data; name="spazi___model___formbean___DateOccupazForm___postBack"

true
------WebKitFormBoundarynkcqVmj0dR7WSFkv
Content-Disposition: form-data; name="spazi___model___formbean___DateOccupazForm___formMode"

FILTER
------WebKitFormBoundarynkcqVmj0dR7WSFkv
Content-Disposition: form-data; name="idaula"

{ID_AULA}
------WebKitFormBoundarynkcqVmj0dR7WSFkv
Content-Disposition: form-data; name="spazi___model___formbean___DateOccupazForm___fromData_day"

{FROM_DAY}
------WebKitFormBoundarynkcqVmj0dR7WSFkv
Content-Disposition: form-data; name="spazi___model___formbean___DateOccupazForm___fromData_month"

{FROM_MESE}
------WebKitFormBoundarynkcqVmj0dR7WSFkv
Content-Disposition: form-data; name="spazi___model___formbean___DateOccupazForm___fromData_year"

{FROM_ANNO}
------WebKitFormBoundarynkcqVmj0dR7WSFkv
Content-Disposition: form-data; name="jaf_spazi___model___formbean___DateOccupazForm___fromData_date_format"

dd/MM/yyyy
------WebKitFormBoundarynkcqVmj0dR7WSFkv
Content-Disposition: form-data; name="spazi___model___formbean___DateOccupazForm___toData_day"

{TO_DAY}
------WebKitFormBoundarynkcqVmj0dR7WSFkv
Content-Disposition: form-data; name="spazi___model___formbean___DateOccupazForm___toData_month"

{TO_MESE}
------WebKitFormBoundarynkcqVmj0dR7WSFkv
Content-Disposition: form-data; name="spazi___model___formbean___DateOccupazForm___toData_year"

{TO_ANNO}
------WebKitFormBoundarynkcqVmj0dR7WSFkv
Content-Disposition: form-data; name="jaf_spazi___model___formbean___DateOccupazForm___toData_date_format"

dd/MM/yyyy
------WebKitFormBoundarynkcqVmj0dR7WSFkv
Content-Disposition: form-data; name="evn_occupazioni"

Visualizza occupazioni
------WebKitFormBoundarynkcqVmj0dR7WSFkv--
"""

s = r.Session()

res = s.post(url, headers=headers, data=multipart_body.encode('utf-8'))

page_html = res.text

print(page_html)
