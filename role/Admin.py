from database import DB, Table, get_info
from datetime import date
import random
database = DB()


class Admin:
    def __init__(self, data_dict, db):
        self.__id = data_dict['ID']
        self.__user = data_dict['username']
        self.__first = data_dict['first']
        self.__last = data_dict['last']
        self.__role = data_dict['role']
        self.__password = data_dict['password']
        self.__db = db

    def __str__(self):
        return (f'Hello {self.__user}. You activate as a {self.__role}\n'
                f'This is the user information\n'
                f'First name: {self.__first}\n'
                f'Last name: {self.__last}\n'
                f'ID: {self.__id}')

    def view_all_student(self):
        if self.__role == 'student':
            print(f"ID: {self.__id} Firstname: {self.__first} Lastname: {self.__last} Role: {self.__role}")

    def view_all_faculty(self):
        if self.__role == 'faculty':
            print(f"ID: {self.__id} Firstname: {self.__first} Lastname: {self.__last} Role: {self.__role}")

    def view_all_project(self):
        i = 0
        projects = self.__db.search('project')
        while i <= len(projects.table):
            project = projects.table[i]
            print(f"ProjectID: {project['ProjectID']} Title: {project['Title']} LeaderID: {project['Lead']} "
                  f"Member1: {project['Member1']} Member2: {project['Member2']} Advisor: {project['Advisor']} "
                  f"Status: {project['Status']}")
            i += 1

    def view_member_pend(self):
        member_pend = self.__db.search('member_pending')
        for member in member_pend.table:
            print(f"ProjectID: {member['ProjectID']}  ")

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

    def __validated_password(self, password):
        return password == self.__password

    def reset_password(self, user):
        password = ''
        for new_digit in range(4):
            password += str(random.randint(1, 9))
        for row in self.__db.search('login').table:
            if row['username'] == user:
                row['password'] = password


