from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin

url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
response = requests.get(url)  # HTML sayfası için istek atıyoruz

soup = BeautifulSoup(response.text, "html.parser")  # HTML sayfasını parçalıyoruz

title = soup.title.string  # Sayfanın başlığını alıyoruz
print(title)

# Sayfanın ilk paragrafını alıyoruz
ilk_paragraf = soup.find_all("p")[0].text 
print("İlk Paragraf:", ilk_paragraf)

for paragraf in soup.find_all("p"):  # Tüm paragrafları alıyoruz
    print(paragraf.text)  # Paragrafları yazdırıyoruz

# İçindekiler bölümünü alıyoruz (Bu site için muhtemelen çalışmayacak)
contents = soup.select('#toc')
for item in contents:
    print(item.text)

# Tüm tabloları ve içeriklerini yazdırıyoruz
tables = soup.find_all("table")
for table in tables:
    table_title = table.caption.text if table.caption else "Tablo başlığı yok"
    print("Tablo Başlığı:", table_title)
    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all(["td", "th"])
        for cell in cells:
            print(cell.text.strip(), end="\t")
        print("")  # Her satırdan sonra yeni bir satıra geç

images = soup.find_all("img")
os.makedirs("downloaded_images", exist_ok=True)
for index, image in enumerate(images):
    image_url = image["src"]  # Resmin URL'sini alıyoruz
    if image_url.startswith("//"):
        image_url = "https:" + image_url
    if not image_url.startswith(("http://", "https://")):
        image_url = urljoin(url, image_url)
    image_response = requests.get(image_url)  # Her resim için ayrı bir istek atıyoruz
    with open(f"downloaded_images/image_{index}.jpg", "wb") as file:
        file.write(image_response.content)  # Resmin içeriğini dosyaya yazıyoruz
    alt_text = image.get("alt", "alternatif metin yok")
    print(f"Resim {index} URL'si: {image_url}")
    print(f"Resim {index} alternatif metin: {alt_text}")
    print(f"Resim {index} indirildi\n" + "-"*50 + "\n")
