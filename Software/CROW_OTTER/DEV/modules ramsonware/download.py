import urllib.request

for m in range(14):
    address_bg = r'https://github.com/AlexanderBissett/Yurii-is-a-idiot/raw/main/temp_img'
    url_slides = fr'{address_bg}/{m}.jpg'
    store_address = fr'C:\Program Files (x86)\Test\{m}.jpg'
    filename, headers = urllib.request.urlretrieve(url_slides, filename = store_address)