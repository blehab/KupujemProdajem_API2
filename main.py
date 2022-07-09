from re import findall
from requests import get
from hashlib import sha1

"""
`API_PATH` i `SIGNATURE` su preuzeti iz zahteva (Chrome Dev Tools -> Network -> Fetch/XHR) koji je poslat na API.
"""

API_PATH = "/api/web/v1/users/ed/139263135"
SIGNATURE = "58a2deae1cc11248fcbf8d5ff1748af1fb0dc2c1"
MAIN_PAGE_URL = "https://novi.kupujemprodajem.com"

def getLinks():
    main_page = get(url=MAIN_PAGE_URL)
    return findall(pattern=r"(?<=src=\")(.*?)(?=\")", string=main_page.text)

def getHash(links: list):
    for link in links:
        data = get(url=MAIN_PAGE_URL + link)
        results = findall(pattern=r"\"(.*?)\"", string=data.text)

        for match in results:
            if sha1(str.encode(API_PATH + match)).hexdigest() == SIGNATURE:
                return match
    
    return ""

if __name__ == "__main__":
    print(getHash(
        links=getLinks()
    ))
