import psycopg2
from tabQ import TecDoc
import csv
from sys import argv
import py7zr
import os
import shutil
import datetime

conn = psycopg2.connect(
    host='localhost',
    user='stepanenko',
    password='Stomatolog',
    database='ddd',
    )
db = conn.cursor()


def create_table(tab_num):
    tab = tecdoc_parse.tables(tab_num)
    column_name = ""
    for col in tab:
        column_name += col["name"] + " nchar(" + str(col["length"]) + "), "

    command_create = "CREATE TABLE IF NOT EXISTS  schema_name.t" + tab_num + " (" + column_name[:-2] + ")"
    db.execute(command_create)
    conn.commit()

    return tab_num


def file_parsing(unpack_file):

    path_to_file = "unpacked_data" + "/" + unpack_file

    with open(path_to_file, "r") as file:
        tab_num = unpack_file[:3]
        tab = tecdoc_parse.tables(tab_num)
        f = open("zzz.csv", "w")
        for row in file:
            step = 0
            string_data = ""
            for column in tab:
                data = row[step:step + column["length"]]
                step += column["length"]
                string_data += data + "|"

            f.writelines(string_data[:-1] + "\n")
        f.close()
    f_csv = open('/home/stepanenko/Projects/xml/xml/zzz.csv', 'r')
    db.copy_from(f_csv, "schema_name.t" + tab_num, sep="|")
    conn.commit()

    # path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'zzz.csv')
    # os.remove(path)


def main(unpak_files, arch_file):
    start = datetime.datetime.now()
    for file in unpak_files:
        if file[-3:] != "GIF":
            create_table(file[:3])
            print(file_parsing(file))
    stop = datetime.datetime.now()
    res = stop - start
    return res
    # shutil.rmtree("unpacked_data")
    # os.remove("archives/" + arch_file)


if __name__ == '__main__':
    t = argv
    version = t[1]
    tecdoc_parse = TecDoc(version)

    archive_direct = os.listdir("archives")
    for arch_file in archive_direct:
        print("Разархивация файлов...", arch_file)

        archive = py7zr.SevenZipFile("archives/" + arch_file, mode='r')
        archive.extract("unpacked_data")
        all_files = os.listdir("unpacked_data")
        print(main(all_files, arch_file))


# with open("ccc.001", "r") as file:
#     tecdoc_parse = TecDoc("Q4")
#     tab = tecdoc_parse.tables("103")
#
#     f = open("zzz.csv", "w")
#     for row in file:
#         step = 0
#         string_data = ""
#         for column in tab:
#             data = row[step:step + column["length"]]
#             step += column["length"]
#             string_data += data + "|"
#
#         f.writelines(string_data[:-1] + "\n")
#     f.close()
# f_csv = open('/home/stepanenko/Projects/xml/xml/zzz.csv', 'r')
# db.copy_from(f_csv, "schema_name.table_name", sep="|")
#
# conn.commit()
# f_csv.close()
#
#
