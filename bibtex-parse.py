'''
Before running, install pybtex using
$ pip3 install pybtex

Purpose: Read in .bib files from ACM IMWUT proceedings and return a CSV with 1 row per paper, parsing relevant info. 
'''
import os
import csv
from pybtex.database.input import bibtex
import pandas as pd
import time
from pybtex.database import parse_file as parser

# Path to the dir
directory_path = os.getcwd() + '/bibtex-files'
csv_directory_path = os.getcwd() + '/bibtex-csvs'

total_rows = 0

# Iterate through all files in the directory
for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)

    # Read the file with pybtex parser
    try:
        bib_data = parser(file_path)
        
        # Extract fields
        fields = []
        if not fields: 
            # Get the first entry
            first_entry_key = next(iter(bib_data.entries))
            first_entry = bib_data.entries[first_entry_key]
            fields = list(first_entry.fields.keys())
            fields.insert(0, 'id')
            fields.insert(1, 'type')
            fields.insert(2, 'authors')

        rows = []
        for key, value in bib_data.entries.items():
            row = {}
            row['id'] = key
            row['type'] = value.type
            row['authors'] = ', '.join([' '.join(filter(None, [' '.join(person.get_part(part)) for part in ['first', 'middle', 'last']]))
                                        for person in value.persons['author']]) if 'author' in value.persons else ''
            for field in fields[3:]:  # Skip 'id', 'type', and 'authors', note id = doi
                row[field] = value.fields.get(field, '')

            rows.append(row)
        print(f'Successfully parsed: {filename}, writing to csv.')
        
        # Write to a CSV file for this file
        csv_file_path = os.path.join(csv_directory_path, f'{os.path.splitext(filename)[0]}.csv')
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

        # print(f'Data written to {csv_file_path}')

        total_rows += len(rows)
    except Exception as e:
        print(f'Failed to parse {filename}: {e}')

# Concat CSVs
print('Supposed length of rows:', total_rows)

df_csv_concat = pd.concat([pd.read_csv(os.path.join(csv_directory_path, file)) for file in os.listdir(csv_directory_path)], ignore_index=True)

# timestr = time.strftime("%Y%m%d-%H%M%S")
csv_master_path = os.path.join(os.getcwd(), f'master_imwut.csv')
df_csv_concat.to_csv(csv_master_path, encoding='utf-8')

print('Actual length of rows:', len(df_csv_concat))

print(f'Successfully written master csv to {csv_master_path}.')



