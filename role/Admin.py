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
                f'This is your user information\n'
                f'First name: {self.__first}\n'
                f'Last name: {self.__last}\n'
                f'ID: {self.__id}')

    def view_advisor_pend(self):
        advisor_pend = self.__db.search('advisor_pending')
        for advisor in advisor_pend.table:
            print(f"ProjectID: {advisor['ProjectID']} From: {advisor['to_be_advisor']}")

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
        return self.__db.search('member_pending').table

    def view_user(self):
        person = self.__db.search('person')
        for person in person.table:
            print(f"ID: {person['ID']} Firstname: {person['first']} Lastname: {person['last']} Role: {person['type']}")

    def create_table(self, table_name):
        self.__db.insert(Table(table_name, []))

    def delete_table(self, table_name):
        self.__db.remove(table_name)

    def delete_row(self, table_name, row_name):
        self.__db.search(table_name).remove(row_name)

    def insert_table(self, table_name):
        self.__db.insert(table_name)

    def insert_row(self, table_name, row_name):
        self.__db.search(table_name).insert(row_name)

    def send_request_committee(self, project_id, faculty_id, faculty_name):
        project = self.__db.search('project')
        project_row = project.filter(lambda x: x['ProjectID'] == project_id)
        login = self.__db.search('login')

        for request in project_row.table:
            print(f"ProjectID: {request['ProjectID']}, Title: {request['Title']}, "
                  f"Lead: {request['Lead']}, Member1: {request['Member1']}, Member2: {request['Member2']}")

    def modify_user_data(self, user_id, respond, new):
        person = self.__db.search('person')
        login = self.__db.search('login')
        person_login = person.join(login, 'ID').table_info

        person_login.get_row(lambda x: x['ID'] == user_id)

        for new_data in person_login.table:
            if respond == 1:
                new_data['username'] = new
            elif respond == 2:
                new_data['first'] = new
            elif respond == 3:
                new_data['last'] = new

    #  If users forget their password
    def reset_password(self, user):
        password = ''
        for new_digit in range(4):
            password += str(random.randint(1, 9))
        for row in self.__db.search('login').table:
            if row['username'] == user:
                row['password'] = password
        print(f"This is your new password: {password}")




