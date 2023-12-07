import csv, os
import random
from datetime import datetime

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def read_csv(csv_file):
    csv_data = []
    with open(os.path.join(__location__, csv_file)) as f:
        rows = csv.DictReader(f)
        for r in rows:
            csv_data.append(dict(r))
    return csv_data


def write_csv(filename, head, db):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(head)
        for dic in db.search(filename).table:
            writer.writerow(dic.values())
        csvfile.close()


def get_info(db, id_person):
    person_info = db.search('person')
    login_data = db.search('login')
    id_data = db.search('ID')
    temp = person_info.join(login_data, id_data)
    for i in temp.table:
        if i['ID'] == id_person:
            return {'ID': i['ID'], 'first': i['first'], 'last': i['last'], 'role': i['role']}
        else:
            continue

def gen_project_id():
    year = datetime.now().year % 100
    class_generation = random.randint(10,99)
    order_number = random.randint(10, 99)
    project_id = f'{year:02d}{class_generation:02d}{order_number:02d}'
    return project_id



# add in code for a Database class
class DB:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None


# add in code for a Table class
import copy


class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table

    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table

    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            temps.append(float(item1[aggregation_key]))
            return function(temps)

    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def insert(self, table):
        self.table.append(table)

    def get_row(self, condition):
        row = 0
        for i in self.table:
            if condition(i):
                return row
            else:
                row += 1

    def head(self, csv_file):
        with open(os.path.join(__location__, csv_file)) as f:
            row_write = csv.reader(f)
            for i in row_write:
                head = i
            return head[0]

    def update(self, row, key, val):
        if row in self.table:
            if key in self.table[row]:
                self.table[row][key] = val



    def __str__(self):
        return self.table_name + ':' + str(self.table)


# modify the code in the Table class so that it supports the insert operation where an entry can be added to a list of dictionary

# modify the code in the Table class so that it supports the update operation where an entry's value associated with a key can be updated

# my_DB = DB()
# person = my_DB.read_csv('persons.csv')
# table1 = Table('persons', person)
# my_DB.insert(table1)
# my_table1 = my_DB.search('persons')
# print(my_table1)
# print(my_DB)
