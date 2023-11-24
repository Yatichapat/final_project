# try wrapping the code below that reads a persons.csv file in a class and make it more general such that it can read in any csv file
import csv, os

# add in code for a Database class
class DB:
    def __init__(self):
        self.database = []

    def read_csv(self, csv_file):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        csv_data = []
        with open(os.path.join(__location__, csv_file)) as f:
            rows = csv.DictReader(f)
            for r in rows:
                csv_data.append(dict(r))
        return csv_data



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
