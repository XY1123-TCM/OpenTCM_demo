"""
Code for processing HERB data
TODO: Implement code for processing HERB data that convert the txt into the database of our format
"""

import sqlite3
import csv

# Read the .txt file
file_path = '../../open-dataset/HERB/HERB_herb_info.txt'
data = []

with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter='\t')
    for row in reader:
        data.append(row)

# Create a SQLite database
db_path = 'herb_info.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a table in the SQLite database
cursor.execute('''
CREATE TABLE IF NOT EXISTS herbs (
    Herb_ID TEXT,
    Herb_pinyin_name TEXT,
    Herb_cn_name TEXT,
    Herb_en_name TEXT,
    Herb_latin_name TEXT,
    Properties TEXT,
    Meridians TEXT,
    UsePart TEXT,
    Function TEXT,
    Indication TEXT,
    Toxicity TEXT,
    Clinical_manifestations TEXT,
    Therapeutic_en_class TEXT,
    Therapeutic_cn_class TEXT,
    TCMID_id TEXT,
    TCM_ID_id TEXT,
    SymMap_id TEXT,
    TCMSP_id TEXT
)
''')
conn.commit()

# Print the first row to debug
if data:
    print(data[0])

# Insert the parsed data into the table
for row in data:
    cursor.execute('''
    INSERT INTO herbs (
        Herb_ID, Herb_pinyin_name, Herb_cn_name, Herb_en_name, Herb_latin_name,
        Properties, Meridians, UsePart, Function, Indication, Toxicity,
        Clinical_manifestations, Therapeutic_en_class, Therapeutic_cn_class,
        TCMID_id, TCM_ID_id, SymMap_id, TCMSP_id
    ) VALUES (
        :Herb_ID, :Herb_pinyin_name, :Herb_cn_name, :Herb_en_name, :Herb_latin_name,
        :Properties, :Meridians, :UsePart, :Function, :Indication, :Toxicity,
        :Clinical_manifestations, :Therapeutic_en_class, :Therapeutic_cn_class,
        :TCMID_id, :TCM_ID_id, :SymMap_id, :TCMSP_id
    )''', row)

conn.commit()
conn.close()











class HerbProcessing:
    def __init__(self, herb_data_path):
        self.herb_data_path = herb_data_path

    def process_herb_data(self):
        pass

    def save_herb_data_to_db(self):
        pass


if __name__ == '__main__':
    herb_data_path = 'path/to/herb/data'
    herb_processing = HerbProcessing(herb_data_path)
    herb_processing.process_herb_data()
    herb_processing.save_herb_data_to_db()
