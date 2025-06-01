import requests
from bs4 import BeautifulSoup
import json

base_url = "https://www.zysj.com.cn"


def get_soup(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'html.parser')


def parse_list_items(ul):
    items = []
    for li in ul.find_all('li', recursive=False):
        item = {}
        span = li.find('span')
        if span:
            item['title'] = span.text.strip()

        a = li.find('a', class_='catalog_group')
        if a:
            item['title'] = a['title']
            item['group_url'] = base_url + a['href']

        a = li.find('a', title=True)
        if a:
            item['title'] = a['title']
            item['url'] = base_url + a['href']

        # Recursively parse sub-lists
        sub_ul = li.find('ul')
        if sub_ul:
            item['children'] = parse_list_items(sub_ul)

        items.append(item)
    return items


def run():
    # Starting URL
    start_url = f"{base_url}/lilunshuji/fuqingzhunvke5190/index.html"
    soup = get_soup(start_url)

    # Find the main catalog
    catalog = soup.find('ul', id='catalog-content')
    if catalog:
        book_structure = parse_list_items(catalog)

    # Convert to JSON
    json_output = json.dumps(book_structure, ensure_ascii=False, indent=4)

    # Print or save JSON
    print(json_output)
    with open('book_structure.json', 'w', encoding='utf-8') as f:
        f.write(json_output)
