from database import DB, Table
from datetime import date
database = DB()


class Admin:
    def __init__(self, data_dict, db, password):
        self.__id = data_dict['ID']
        self.__user = data_dict['user']
        self.__first = data_dict['first']
        self.__last = data_dict['last']
        self.__role = data_dict['role']
        self.__db = db
        self.__password = password

    def __str__(self):
        return (f'Hello {self.__user}. You activate as a {self.__role}\n'
                f'This is the user information\n'
                f'First name: {self.__first}\n'
                f'Last name: {self.__last}\n'
                f'ID: {self.__id}')

    def view_database(self):
        return self.__db

    def create_table(self, table_name):
        self.__db.insert(Table(table_name, []))

    def delete_table(self, table_name):
        self.__db.remove(table_name)

    def delete_row(self, table_name, row_name):
        self.__db.search(table_name).remove(row_name)

    def update(self, table_name, row, key, val):
        self.__db.search(table_name).update(row, key, val)

    def insert_table(self, table_name):
        self.__db.insert(table_name)

    def insert_row(self, table_name, row_name):
        self.__db.search(table_name).insert(row_name)

#  If users forget their password
    def reset_password(self, new_password):
        self.__password = new_password
        print(f'Password for user {self.__user} has been reset')

    def validated_password(self, password):
        return password == self.__password
