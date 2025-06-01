import sqlite3

# Step 1: Open and read from both databases, excluding Herb_ID from herb_info.db
conn_info = sqlite3.connect('herb_info.db')
conn_tcm = sqlite3.connect('../db/tcm.db')

cursor_info = conn_info.cursor()
cursor_tcm = conn_tcm.cursor()

# Fetch data from herb_info.db, excluding Herb_ID
cursor_info.execute('''
SELECT Herb_pinyin_name, Herb_cn_name, Herb_en_name, Herb_latin_name,
       Properties, Meridians, UsePart, Function, Indication, Toxicity,
       Clinical_manifestations, Therapeutic_en_class, Therapeutic_cn_class,
       TCMID_id, TCM_ID_id, SymMap_id, TCMSP_id
FROM herbs
''')
herb_info_data = cursor_info.fetchall()
herb_info_columns = [description[0] for description in cursor_info.description]

# Fetch data from tcm.db
cursor_tcm.execute('SELECT * FROM herb')
herb_tcm_data = cursor_tcm.fetchall()
herb_tcm_columns = [description[0] for description in cursor_tcm.description]

conn_info.close()
conn_tcm.close()

# Step 2: Create a new database and combined herb table
conn_joined = sqlite3.connect('../db/tcm.db')
cursor_joined = conn_joined.cursor()

# Combine the columns, ensuring no duplicate Herb_ID and discarding Herb_cn_name
combined_columns = herb_tcm_columns + [col for col in herb_info_columns if col != 'Herb_cn_name']
combined_columns_sql = ', '.join([f'{col} TEXT' for col in combined_columns])

create_table_sql = f'''
CREATE TABLE IF NOT EXISTS herbJoined (
    {combined_columns_sql}
)
'''

cursor_joined.execute(create_table_sql)
conn_joined.commit()

# Step 3: Generate unique herb_id values for new rows
def generate_unique_herb_id(existing_ids):
    new_id = 1
    while new_id in existing_ids:
        new_id += 1
    existing_ids.add(new_id)
    return new_id

existing_herb_ids = {row[0] for row in herb_tcm_data}  # Assuming the first column is herb_id

# Prepare the insertion SQL
insert_sql = f'''
INSERT INTO herbJoined ({', '.join(combined_columns)}) 
VALUES ({', '.join(['?' for _ in combined_columns])})
'''

# Create a dictionary for herb_info data with Herb_cn_name as the key
herb_info_dict = {row[1]: row for row in herb_info_data}

# Insert data from tcm.db, merging with herb_info.db where names match
for row in herb_tcm_data:
    name = row[1]  # Assuming the second column is the 'name' column
    if name in herb_info_dict:
        info_row = herb_info_dict[name]
        new_row = list(row) + [info_row[herb_info_columns.index(col)] for col in herb_info_columns if col != 'Herb_cn_name']
    else:
        new_row = list(row) + [None] * (len(herb_info_columns) - 1)
    cursor_joined.execute(insert_sql, new_row)

# Insert remaining data from herb_info.db that didn't match any row in tcm.db
for row in herb_info_data:
    if row[1] not in [r[1] for r in herb_tcm_data]:
        new_row = [None] * len(herb_tcm_columns)
        new_row[herb_tcm_columns.index('name')] = row[1]  # Insert Herb_cn_name into the name column
        new_row[herb_tcm_columns.index('herb_id')] = generate_unique_herb_id(existing_herb_ids)  # Generate unique herb_id
        new_row += [row[herb_info_columns.index(col)] for col in herb_info_columns if col != 'Herb_cn_name']
        cursor_joined.execute(insert_sql, new_row)

conn_joined.commit()
conn_joined.close()
