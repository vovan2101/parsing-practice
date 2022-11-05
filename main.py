# import requests
# from bs4 import BeautifulSoup

# with open("blank/index.html") as file:
#     src = file.read()
# print(src)

# soup = BeautifulSoup(src, "lxml")

# title = soup.title
# print(title)
# print(title.text)
# print(title.string)

# .find() .find_all()
# page_h1 = soup.find("h1")
# print(page_h1)
#
# page_all_h1 = soup.find_all("h1")
# print(page_all_h1)
#
# for item in page_all_h1:
#     print(item.text)

# user_name = soup.find("div", class_="user__name")
# print(user_name.text.strip())

# user_name = soup.find(class_="user__name").find("span").text
# print(user_name)

# user_name = soup.find("div", {"class": "user__name", "id": "aaa"}).find("span").text
# print(user_name)

# find_all_spans_in_user_info = soup.find(class_="user__info").find_all("span")
# print(find_all_spans_in_user_info)

# for item in find_all_spans_in_user_info:
#     print(item.text)

# print(find_all_spans_in_user_info[0])
# print(find_all_spans_in_user_info[2].text)

# social_links = soup.find(class_="social__networks").find("ul").find_all("a")
# print(social_links)

# all_a = soup.find_all("a")
# print(all_a)
#
# for item in all_a:
#     item_text = item.text
#     item_url = item.get("href")
#     print(f"{item_text}: {item_url}")

# .find_parent() .find_parents()

# post_div = soup.find(class_="post__text").find_parent()
# print(post_div)

# post_div = soup.find(class_="post__text").find_parent("div", "user__post")
# print(post_div)

# post_divs = soup.find(class_="post__text").find_parents("div", "user__post")
# print(post_divs)

# .next_element .previous_element
# next_el = soup.find(class_="post__title").next_element.next_element.text
# print(next_el)
#
# next_el = soup.find(class_="post__title").find_next().text
# print(next_el)

# .find_next_sibling() .find_previous_sibling()
# next_sib = soup.find(class_="post__title").find_next_sibling()
# print(next_sib)

# prev_sib = soup.find(class_="post__date").find_previous_sibling()
# print(prev_sib)

# post_title = soup.find(class_="post__date").find_previous_sibling().find_next().text
# print(post_title)

# links = soup.find(class_="some__links").find_all("a")
# print(links)
#
# for link in links:
#     link_href_attr = link.get("href")
#     link_href_attr1 = link["href"]
#
#     link_data_attr = link.get("data-attr")
#     link_data_attr1 = link["data-attr"]
#
#     print(link_href_attr1)
#     print(link_data_attr1)

# find_a_by_text = soup.find("a", text="Одежда")
# print(find_a_by_text)
#
# find_a_by_text = soup.find("a", text="Одежда для взрослых")
# print(find_a_by_text)

# find_a_by_text = soup.find("a", text=re.compile("Одежда"))
# print(find_a_by_text)

# find_all_clothes = soup.find_all(text=re.compile("([Оо]дежда)"))
# print(find_all_clothes)



# url = 'https://commons.wikimedia.org/wiki/File:'
# end_points = ['AKC 2014 pics7 019.jpg', '4-4-0 Inyo.jpg']

# for end_point in end_points:
#     images_url = url + end_point


# req = requests.get(images_url)
# src = req.text

# soup = BeautifulSoup(src, 'lxml')
# images = soup.find(class_ = 'description mw-content-ltr en').text[10:]

import requests
from bs4 import BeautifulSoup
import json


# User put info about event that they looking for
state = str(input('Please enter state: '))
print()
city = str(input('Please enter city name: '))
print()
event_name = str(input('Please enter an event name: '))
print()
search = f'https://nominatim.openstreetmap.org/ui/search.html?q={state}+{city}+{event_name}'


# Taking osm id of event, so I can get more data about event
search_json = requests.get(f'https://nominatim.openstreetmap.org/search.php?q={state}+{city}+{event_name}&format=jsonv2')
osm_id_data = json.loads(search_json.text)
osm_id = osm_id_data[0]['osm_id']


# All data from json page
advanced_search_json = requests.get(f'https://nominatim.openstreetmap.org/details.php?osmtype=W&osmid={osm_id}&format=json')
data = json.loads(advanced_search_json.text)

place_id = data['place_id']
category = data['category']
experience_name = data['names']['name']
address_1 = data['addresstags']['street']
address_2 = data['addresstags']['housenumber']
city = data['addresstags']['city']
state = data['addresstags']['state']
zip = data['addresstags']['postcode']
wikipedia_name = data['calculated_wikipedia'][2:]


# Taking first paragraph from wikipedia if more then 50 elements, else taking two paragraphs
wikipedia = f'https://en.wikipedia.org/wiki/{wikipedia_name}'
wikipedia_request = requests.get(wikipedia)
soup_wikipedia = BeautifulSoup(wikipedia_request.text, 'lxml')
paragraph1 = soup_wikipedia.find('p').text.strip()

if len(paragraph1) < 50:
    paragraph2 = soup_wikipedia.find('p').find_next('p').text.strip()
try:
    experience_description = f'{paragraph1}\n\n{paragraph2}'
except:
    experience_description = paragraph1


# All event images links and titles
images_url = requests.get(f'https://commons.wikimedia.org/wiki/Category{wikipedia_name}')
soup_images = BeautifulSoup(images_url.text, 'lxml')
images_wikimedia = soup_images.find('ul', class_ ='gallery mw-gallery-traditional')

list_images = []
for image in images_wikimedia.find_all('li', class_ = 'gallerybox'):
    images_title = image.find('a').get('href')
    images = f'https://en.wikipedia.org/{images_title}'
    list_images.append(images)



# All data about event
all_info = {
    'place_id' : place_id,
    'category' : category,
    'experience_name': experience_name,
    'city' : city,
    'state' : state,
    'zip': zip,
    'address1': address_1,
    'address2' : address_2,
    'wikipedia_name' : wikipedia,
    'experience_description' : experience_description,
    'images' : list_images,
}

with open('all_info_json', 'w') as file:
    json.dump(all_info, file, indent=4, ensure_ascii=False)


# Images description
images_description_url = requests.get(f'https://commons.wikimedia.org{images_title}')
soup_description = BeautifulSoup(images_description_url.text, 'lxml')
description_wikimedia = soup_description.find('tbody').find('td', class_ = 'description')
for description in description_wikimedia.find_all('div', class_ = 'description mw-content-ltr en'):
    images_description = description.text
    print(images_description)