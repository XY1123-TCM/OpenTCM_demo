"""
Preprocessor for Traditional Chinese Medicine (TCM) books

The books are of format:
======Title======

<book> # Metadata
書名=傅青主女科
作者=傅山
朝代=清
年份=
分類=婦科
品質=0%
</book>

Table of content

======Chapter 1======
=====Section 1=====
====Subsection 1====
Content
...

"""

import os
import pandas as pd
import sqlite3  # SQLite is used to store the data
import zhconv  # Convert between simplified and traditional Chinese
import util
import yaml


def init_db(create_new=False):
    """
    Initialize the SQLite database
    :return:
    """
    conn = sqlite3.connect('../db/tcm.db')
    if not create_new:
        return
    # drop the tables if they exist
    conn.execute('DROP TABLE IF EXISTS metadata')
    conn.execute('DROP TABLE IF EXISTS book')

    # create the tables
    conn.execute('''
    CREATE TABLE metadata (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_title TEXT,
        author TEXT,
        dynasty TEXT,
        year TEXT,
        category TEXT,
        quality TEXT,
        version TEXT,
        reference TEXT,
        notes TEXT
    )
    ''')
    conn.execute('''
    CREATE TABLE book (
        ref_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        chapter_id INTEGER,
        section_id TEXT,
        chapter TEXT,
        section TEXT,
        content TEXT
    )
    ''')
    conn.close()


def post_process_content(content):
    """
    Post-process the content
    :param content: str
    :return: str
    """
    # Remove the spaces and newlines at the beginning and end of the content
    content = content.strip()
    return content


class Preprocessor:
    """
    Preprocessor for Traditional Chinese Medicine (TCM) books
    ----------
    load_data: Load data from the data directory
    preprocess: Preprocess the data
    """

    def __init__(self,
                 data_dir,
                 db_path=None,
                 book_id=0,
                 chapter_break="======",
                 section_break="=====",
                 remove_title_number=False
                 ):
        self.book_id = book_id
        self.data_dir = data_dir
        self.raw_data = None
        self.metadata = None
        self.book = None
        self.chapter_break = chapter_break
        self.section_break = section_break
        self.remove_title_number = remove_title_number
        if db_path:
            self.db_path = db_path
        else:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            db_dir = os.path.join(current_dir, '../db')
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)
            self.db_path = os.path.join(db_dir, 'tcm.db')

    def load_data(self):
        """
        Load text data from the txt file and convert it to metadata and book dataframes
        :return:
        """
        # Load the raw data
        file_path = os.path.join(self.data_dir, 'index.txt')
        with open(file_path, 'r', encoding='utf-8') as f:
            self.raw_data = f.read()
        # Convert to simplified Chinese
        self.raw_data = zhconv.convert(self.raw_data, 'zh-cn')

        # Extract metadata from the raw data
        self.extract_metadata()
        self.extract_book()

    def extract_metadata(self):
        """
        Extract metadata from the raw data
        :return:
        """
        # Extract metadata from the raw data
        metadata = {'book_id': self.book_id}
        metadata_start = self.raw_data.find('<book>')
        metadata_start += len('<book>')
        metadata_end = self.raw_data.find('</book>')
        metadata_str = self.raw_data[metadata_start:metadata_end]
        metadata_list = metadata_str.split('\n')
        metadata_list = [item.strip() for item in metadata_list if item.strip()]

        for item in metadata_list:
            key, value = item.split('=')
            # Replace the keys with English names
            if key == '书名':
                key = 'book_title'
            elif key == '作者':
                key = 'author'
            elif key == '朝代':
                key = 'dynasty'
            elif key == '年份':
                key = 'year'
            elif key == '分类':
                key = 'category'
            elif key == '品质':
                key = 'quality'
            elif key == '版本':
                key = 'version'
            elif key == '参本':
                key = 'reference'
            elif key == '备考':
                key = 'notes'
            metadata[key] = value
        self.metadata = metadata

    def extract_book(self):
        """
        Extract book content from the raw data
        :return:
        """
        # Extract book content from the raw data
        book_start = self.raw_data.find('</book>')
        book_start += len('</book>')
        book_str = self.raw_data[book_start:]
        book_str = book_str.strip()
        book_lines = book_str.split('\n')

        # Remove \\from each line
        book_lines = [line.replace('\\', '') for line in book_lines]
        book_lines = [line.strip() for line in book_lines]

        # Convert the book content to a dataframe of chapter_id, chapters, section_id, sections, and content
        book = []
        chapter = None
        section = None
        chapter_id = 0
        section_id = 0
        content = []
        for line in book_lines:
            if line.startswith(self.chapter_break):
                # Processing the chapter
                if content:
                    book.append({
                        'book_id': self.book_id,
                        'chapter_id': chapter_id,
                        'section_id': section_id,
                        'chapter': chapter,
                        'section': section,
                        'content': post_process_content("\n".join(content))
                    })
                content = []
                line = line.replace('=', '')
                line = line.strip()
                chapter = line
                chapter_id += 1
                section_id = 0
            elif line.startswith(self.section_break):
                # Processing the section
                if content:
                    book.append({
                        'book_id': self.book_id,
                        'chapter_id': chapter_id,
                        'section_id': section_id,
                        'chapter': chapter,
                        'section': section,
                        'content': post_process_content("\n".join(content))
                    })
                content = []
                line = line.replace('=', '')
                line = line.strip()
                section = line
                section_id += 1
            else:
                # Processing the content
                content.append(line)
                if content == ['']:
                    content = []
        if content:
            book.append({
                'book_id': self.book_id,
                'chapter_id': chapter_id,
                'section_id': section_id,
                'chapter': chapter,
                'section': section,
                'content': post_process_content("\n".join(content))
            })

        # TODO: Update the content to limit the length of each. Split the content into multiple if it is too long

        # Export the book to markdown format
        title = self.metadata['book_title']
        export_path = os.path.join("../../books/markdown", f'{title}.md')

        with open(export_path, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n")
            for row in book:
                f.write(f"## {row['chapter']}\n")
                f.write(f"### {row['section']}\n")
                f.write(row['content'])
                f.write('\n\n')

        if self.remove_title_number:
            for idx, row in enumerate(book):
                book[idx]['chapter'] = util.remove_number(book[idx]['chapter'])
                book[idx]['section'] = util.remove_number(book[idx]['section'])

        self.book = pd.DataFrame(book)

    def get_results(self):
        """
        Get the metadata and book content
        :return: metadata, book
        """
        return self.metadata, self.book

    def save_to_sqlite(self):
        """
        Save the metadata and book content to a SQLite database
        :return:
        """
        conn = sqlite3.connect(self.db_path)

        # Convert the metadata to a row in the metadata table
        metadata = pd.DataFrame([self.metadata])
        # Append the metadata to the metadata table with key=book_id
        # If exists, replace the row
        metadata.to_sql('metadata', conn, if_exists='replace', index=False)

        column_count = len(self.book.columns)
        # Check the type of each column in the book dataframe
        for col in self.book.columns:
            if self.book[col].dtype == 'O':
                self.book[col] = self.book[col].astype(str)

        # If exists, remove this book in the table, then append the new book
        conn.execute(f'DELETE FROM book WHERE book_id = {self.book_id}')

        self.book.to_sql('book', conn, if_exists='append', index=False)

        # Log the summary
        print(f"Metadata: {metadata.shape[0]} rows")
        print(f"Book: {self.book.shape[0]} rows")
        print(f"Columns: {column_count} columns")
        conn.close()

    def book_to_sqlite(self):
        """
        Load the book, preprocess it, and save it to SQLite
        :return:
        """
        self.load_data()
        self.save_to_sqlite()


def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def run(config):
    preprocessor = Preprocessor(
        data_dir=config['data_dir'],
        db_path=config['db_path'],
        book_id=config['book_id'],
        chapter_break=config['chapter_break'],
        section_break=config['section_break'],
        remove_title_number=config['remove_title_number']
    )
    preprocessor.book_to_sqlite()


if __name__ == '__main__':
    init_db(create_new=True)
    config_ = load_config("../config/傅青主女科.yaml")
    run(config_)
    config_ = load_config("../config/傷寒雜病論_桂本.yaml")
    run(config_)
