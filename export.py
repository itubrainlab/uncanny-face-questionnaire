import sqlite3
import website
from os import path, mkdir
import csv
from datetime import datetime

EXPORT_FOLDER = 'export'


def table_to_csv(timestamp, cur, table_name):
    cur.execute("SELECT * FROM " + table_name)
    rows = cur.fetchall()
    with open(path.join(EXPORT_FOLDER, timestamp + '_' + table_name + '.csv'), 'w') as ouput_file:
        file_writer = csv.writer(ouput_file)
        for r in rows:
            file_writer.writerow(r)
        ouput_file.close()


if __name__ == '__main__':
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')

    if not path.exists(EXPORT_FOLDER):
        mkdir(EXPORT_FOLDER)

    with sqlite3.connect(path.join(website.INSTANCE_FOLDER, website.DB_NAME)) as conn:
        cur = conn.cursor()
        table_to_csv(timestamp, cur, 'user')
        table_to_csv(timestamp, cur, 'rating')
        table_to_csv(timestamp, cur, 'submit')
