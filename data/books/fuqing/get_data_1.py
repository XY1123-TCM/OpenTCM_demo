"""
Read the json file and store the "content" into a hierarchical structure
"""

import requests
from bs4 import BeautifulSoup
import json


def create_dir(path):
    import os
    if not os.path.exists(path):
        os.makedirs(path)


def text_filter(text):
    # remove the empty lines
    text = text.strip()
    return text


def get_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find('div', id='content')
    return text_filter(content.text)


def get_book(file_path):
    with open(file_path, 'r') as file:
        book = json.load(file)

    # iterate through each chapter and section to download the content from url
    for chapter in book:
        if 'children' in chapter:
            for section in chapter['children']:
                if 'url' in section and "group" not in section['url']:
                    section['content'] = get_content(section['url'])
                # if the section has children, download the content for each child
                if 'children' in section:
                    for child in section['children']:
                        if 'url' in child and "group" not in child['url']:
                            child['content'] = get_content(child['url'])
        else:
            if 'url' in chapter and "group" not in chapter['url']:
                chapter['content'] = get_content(chapter['url'])
    # print(book)
    return book


def get_markdown(book):
    """
    Convert the json book content into markdown format
    :param book:
    :return:
    """
    markdown = ''
    for chapter in book:
        markdown += f"# {chapter['title']}\n\n"
        if 'content' in chapter:
            markdown += f"{chapter['content']}\n\n"
        if 'children' in chapter:
            for section in chapter['children']:
                markdown += f"## {section['title']}\n\n"
                if 'content' in section:
                    markdown += f"{section['content']}\n\n"
                if 'children' in section:
                    for child in section['children']:
                        markdown += f"### {child['title']}\n\n"
                        if 'content' in child:
                            markdown += f"{child['content']}\n\n"
    return markdown


def create_index(book):
    """
    Create a book index for table of content
    :param book:
    :return:
    """
    index = ''
    for chapter in book:
        index += f"* {chapter['title']}"
        if 'children' in chapter:
            index += '\n'
            for section in chapter['children']:
                index += f"  * {section['title']}"
                if 'children' in section:
                    index += '\n'
                    for child in section['children']:
                        index += f"    * {child['title']}\n"
                else:
                    index += '\n'
        else:
            index += '\n'
    return index


if __name__ == '__main__':
    file_path = 'book_structure.json'
    book = get_book(file_path)
    # save to a new json file
    with open('book_content.json', 'w') as file:
        json.dump(book, file, indent=4, ensure_ascii=False)
    # convert the book content to markdown format
    markdown = get_markdown(book)
    with open('book_content.md', 'w') as file:
        file.write(markdown)
    # create a book index
    index = create_index(book)
    print(index)
    with open('book_index.md', 'w') as file:
        file.write(index)
