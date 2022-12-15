import sqlite3
import website
from os import path, mkdir
import csv
from datetime import datetime

EXPORT_FOLDER = 'export'


def table_to_csv(cur, table_name):
    cur.execute("SELECT * FROM " + table_name)
    rows = cur.fetchall()
    print(table_name + " rows: " + str(len(rows)))
    if len(rows) > 0:
        print(table_name + " last_row: " + str(rows[-1]))


if __name__ == '__main__':
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')

    if not path.exists(EXPORT_FOLDER):
        mkdir(EXPORT_FOLDER)

    with sqlite3.connect(path.join('website', website.DB_NAME)) as conn:
        cur = conn.cursor()
        table_to_csv(cur, 'user')
        table_to_csv(cur, 'rating')
        table_to_csv(cur, 'submit')
