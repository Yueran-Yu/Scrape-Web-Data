import requests
from bs4 import BeautifulSoup
import pprint
import json
import os.path

movies_item_dict = dict()
commedy_links = []
for i in range(1, 5):
    drama = requests.get('https://www.twilighttimemovies.com/genre/comedy/?sort=featured&page=' + str(i))
    soup = BeautifulSoup(drama.content, 'html.parser')
    items = soup.findAll("figure", {"class": "card-figure"})
    for item in items:
        a = item.find("a", href=True)
        if a is None:
            continue
        commedy_links.append(a['href'])
        # print(a['href'])

id = 1

for line in commedy_links:
    # print(line)
    inner_page = requests.get(line)
    soup = BeautifulSoup(inner_page.content, 'html.parser')
    title = soup.find("h1").text
    # print(title)
    try:
        description = soup.find("div", {"class": "descrip"}).findAll("em")[0].text
    except:
        pass
    try:
        description = soup.find("div", {"class": "descrip"}).findAll("div")[0].text
    except:
        pass
    try:
        description = soup.find("div", {"class": "descrip"}).text
    except:
        pass
    try:
        price = soup.find("span", {"class": "price"}).text.strip().lstrip("$")
    except:
        price = ''
    img_link = soup.find("li", {"class": "productView-thumbnail"}).find("img")['src']
    # print("title: " + title)
    # print("Description: " + description)
    # print("Price: " + price)
    # print(img_link)
    movies_item_dict.update(
        {id: {'name': title, 'description': description, 'price': price, 'img_link': img_link,  'category': 'Commedy'}})
    id += 1

pprint.pprint(movies_item_dict)

with open(os.path.join('Outputs', 'commedy.json'), 'w') as fp:
    json.dump(movies_item_dict, fp, indent=4)
