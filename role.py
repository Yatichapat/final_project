from database import DB, Table, gen_project_id
from datetime import date
database = DB()

class Student:
    def __init__(self, dict, db):
        self.__id = dict['ID']
        self.__user = dict['user']
        self.__fist = dict['first']
        self.__last = dict['last']
        self.__role = dict['role']
        self.__db = db

    def see_request_pending(self):
        print(self.__db.search('Member_pending_request').table)

    def respond_request(self, project_id, respond):
        member_pending = self.__db.search('Member_pending_request')
        project = self.__db.search('project')
        login = self.__db.search('login')

        member_pending_row = member_pending.get_row(lambda x: x['ProjectID'] == project_id and x['ID'] == self.__id)
        project_row = project.get_row(lambda x: x['ProjectID'] == project_id)
        login_row = login.get_row(lambda x: x['ID'] == self.__id)
        member_pending.update(member_pending_row, 'Response_date', date.today())
        while True:
            if respond == 'A':
                member_pending.update(member_pending_row, 'Response', 'Accept')
                login.update(login_row, 'role', 'member')
                if project.table[project_row]['Member1'] == '-':
                    project.update(project_row, 'Member1', f'{self.__id}{self.__fist}')
                    break
                else:
                    project.update(project_row, 'Member2', f'{self.__id}{self.__fist}')
                    break
            elif respond == 'D':
                member_pending.update(member_pending_row, 'Response', 'Deny')
                break
            else:
                print('Your option is none in above. Please enter your choice again.')
                continue

    def create_project(self, title):
        new_proj = {
            'ProjectID': gen_project_id(),
            'Title': title,
            'Lead': f'{self.__id}{self.__fist}',
            'Member1': '-',
            'Member2': '-',
            'Advisor': '-',
            'Status': 'Processing'
        }
        self.__db.search('project').insert(new_proj)
        login = self.__db.search('login')
        login_row = login.get_row(lambda x: x['ID'] == self.__id)
        login.update(login_row, 'role', 'lead')

