"""
Use LLM to extract the herb, disease, symptom, and treatment information from the database
"""
import logging

from llm_util import get_bedrock_response, llm_post_processor, get_chatgpt_response

import sqlite3
import pandas as pd
import json
import tqdm
import multiprocessing as mp
import numpy as np

## Set logging level to debug
logging.basicConfig(level=logging.DEBUG)


def get_treatment(text):
    """
    Get the list of herbs from the text
    """
    user_message = """
请将以下中医书本内容重新整理为单个JSON格式，包括以下字段：

- `disease`: Name of the disease.
- `symptoms`: Description of the symptoms.
- `prescription_name`: Name of the prescription.
- `herbs`: List of herbs used in the prescription.
  - `name`: Name of the herb.
  - `dosage`: Dosage amount of the herb.
  - `preparation`: Preparation method of the herb.
- `notes`: Additional notes on the prescription and its effects.

可能包含多个处方，每个处方包含一个疾病、症状、处方名称、草药列表和备注。
章节名称可能包含数字，如“產後肝痿七十五”，请将数字去掉，只保留中文部分。

回复单个JSON，不要带“```”，JSON格式的示例：

```
[{
  "disease": "赤帶下",
  "symptoms": "婦人有帶下而色紅者，似血非血，淋瀝不斷",
  "prescription_name": "清肝止淋湯",
  "herbs": [
    {
      "name": "白芍",
      "dosage": "一两",
      "preparation": "醋炒"
    },
    {
      "name": "當歸",
      "dosage": "一两",
      "preparation": "酒洗"
    }
  ],
  "notes": "水煎服，一劑少止..."
},
{
    "disease": "Another Disease",
    ...
}
]
```

仅回复JSON内容，如果不是处方，回复 "[]"。无需加其他note或者其他内容，只需回复JSON格式的内容。

书本内容：
"""
    user_message += text
    # response_text = get_bedrock_response(user_message, max_gen_len=2048)
    response_text = get_chatgpt_response(user_message, model_name="gpt-4o", max_tokens=None)
    response_json = llm_post_processor(response_text)
    return response_json


def create_treatment_table(create_new=False):
    """
    Create the treatment table in the SQLite database
    """
    if not create_new:
        return
    conn = sqlite3.connect('../db/tcm.db')
    cursor = conn.cursor()
    # Drop the treatment table if it exists
    cursor.execute('DROP TABLE IF EXISTS treatment')
    conn.commit()
    # Create the treatment table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS treatment (
        treatment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ref_id INTEGER,
        disease TEXT,
        symptoms TEXT,
        prescription_name TEXT,
        herbs TEXT,
        notes TEXT
    )
    ''')
    conn.commit()
    conn.close()


class LLMProcessor2:
    def __init__(self, db_path, book_id):
        """
        Initialize the LLMProcessor
        :param db_path: str
            Path to the SQLite database
        :param book_id: int
            Book ID for processing
        """
        self.db_path = db_path
        self.book_id = book_id

    def process_row(self, row, db_path, skip_processed=True):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        if skip_processed:
            # Check if the row has already been processed in the treatment table
            cursor.execute('SELECT COUNT(*) FROM treatment WHERE ref_id = ?', (row['ref_id'],))
            count = cursor.fetchone()[0]
            if count > 0:
                conn.close()
                logging.info(f"Skipping row {row['ref_id']}")
                return

        if row['chapter'] == 'None':
            return
        content = row['content']
        chapter_info = f'# Chapter: {row["chapter"]}\n'
        section_info = f'## Section: {row["section"]}\n'
        content = chapter_info + section_info + content

        response_json = get_treatment(content)

        if response_json:
            for treatment in response_json:
                herbs = treatment['herbs']
                herbs_str = json.dumps(herbs, ensure_ascii=False)
                cursor.execute('''
                INSERT INTO treatment (ref_id, disease, symptoms, prescription_name, herbs, notes)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (row['ref_id'], treatment['disease'], treatment['symptoms'], treatment['prescription_name'],
                      herbs_str, treatment['notes']))

                logging.info(f"Inserted treatment for ref_id {row['ref_id']}")

            conn.commit()
        conn.close()
        logging.info(f"Processed ref_id {row['ref_id']}")

    def worker(self, rows, db_path):
        for idx, row in rows.iterrows():
            self.process_row(row, db_path)

    def process_books(self, max_rows=None):
        """
        Convert the book to a set of treatments
        From the ref database (book), we extract the corresponding information of herb, disease, symptom, and treatment
        Each row in the book table contains the following columns:
            ref_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            chapter_id INTEGER,
            section_id TEXT,
            chapter TEXT,
            section TEXT,
            content TEXT
        Steps:
            1. Get the content from the book table
            2. Extract the herb, disease, symptom, and treatment information using LLM
            3. Create new tables for the extracted information
        """

        # Get the content from the book table
        query = f"SELECT * FROM book WHERE book_id = {self.book_id}"
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()

        if max_rows:
            # Process only a subset of rows
            df = df.head(max_rows)

        logging.info(f"Processing {df.shape[0]} rows")

        # Split dataframe into chunks
        num_processes = mp.cpu_count()
        chunks = np.array_split(df, num_processes)

        with mp.Pool(processes=num_processes) as pool:
            print(f"Processing {num_processes} chunks")
            pool.starmap(self.worker, [(chunk, self.db_path) for chunk in chunks])


def update_herb_table(create_new=False):
    """
    Create or update the herb table in the SQLite database from the treatment table.
    """

    conn = sqlite3.connect('../db/tcm.db')
    cursor = conn.cursor()

    if create_new:
        # Drop the existing tables if requested to create new
        cursor.execute('DROP TABLE IF EXISTS herb')
        cursor.execute('DROP TABLE IF EXISTS herb_ref')
        conn.commit()

        # Create the herb table
        cursor.execute('''
        CREATE TABLE herb (
            herb_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT
        )
        ''')
        conn.commit()

        # Create the herb_ref table
        cursor.execute('''
        CREATE TABLE herb_ref (
            herb_id INTEGER,
            treatment_id INTEGER,
            ref_id INTEGER,
            dosage TEXT,
            preparation TEXT,
            UNIQUE(herb_id, treatment_id, ref_id)
        )
        ''')
        conn.commit()

    # Iterate through the treatment table and insert the data
    cursor.execute('SELECT treatment_id, ref_id, herbs FROM treatment')
    rows = cursor.fetchall()
    for row in rows:
        herbs = json.loads(row[2])
        for herb in herbs:
            herb.setdefault('dosage', '')
            herb.setdefault('preparation', '')

            # Check if the herb already exists in the herb table
            cursor.execute('SELECT herb_id FROM herb WHERE name = ?', (herb['name'],))
            herb_id = cursor.fetchone()
            if herb_id:
                herb_id = herb_id[0]
            else:
                # Insert new herb if it doesn't exist
                cursor.execute('INSERT INTO herb (name, description) VALUES (?, ?)', (herb['name'], ''))
                herb_id = cursor.lastrowid

            # Check if the ref_id already exists for this herb_id and treatment_id
            cursor.execute('''
                SELECT 1 FROM herb_ref WHERE herb_id = ? AND treatment_id = ? AND ref_id = ?
            ''', (herb_id, row[0], row[1]))
            if not cursor.fetchone():
                # Insert into herb_ref only if the combination does not exist
                cursor.execute('''
                    INSERT INTO herb_ref (herb_id, treatment_id, ref_id, dosage, preparation) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (herb_id, row[0], row[1], herb['dosage'], herb['preparation']))

    conn.commit()
    logging.info('Herb table updated successfully')


def test_processor():
    """
    Test the LLMProcessor
    """
    create_treatment_table(create_new=False)
    processor = LLMProcessor2('../db/tcm.db', book_id=1)
    processor.process_books(max_rows=10)
    update_herb_table(create_new=False)


def run():
    """
    Process the data using LLM
    """
    create_treatment_table(create_new=False)
    processor = LLMProcessor2('../db/tcm.db', book_id=1)
    processor.process_books()
    update_herb_table(create_new=False)


if __name__ == '__main__':
    test_processor()
    # run()
