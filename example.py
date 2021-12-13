from img_catalog import IMGCatalog

import requests

if __name__ == '__main__':
    catalog = IMGCatalog()
    response = requests.get('http://localhost:8080/?')
    print(response.content)
    response = requests.get('http://localhost:8080/?')
    print(response.content)
