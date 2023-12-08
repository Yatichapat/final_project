from database import DB, Table, gen_project_id
from datetime import date
database = DB()


class Faculty:

    def __init__(self, data_dict, db):
        self.__id = data_dict['ID']
        self.__user = data_dict['user']
        self.__first = data_dict['first']
        self.__last = data_dict['last']
        self.__role = data_dict['role']
        self.__db = db

    def __str__(self):
        return (f'Hello {self.__user}. You activate as a {self.__role}\n'
                f'This is the user information\n'
                f'First name: {self.__first}\n'
                f'Last name: {self.__last}\n'
                f'ID: {self.__id}')

    def see_request_advisor(self):
        return self.__db.search('Advisor_pending_request.csv').table

    def respond_advisor_request(self, project_id, respond):
        advisor_pending = self.__db.search('Advisor_pending_request.csv')
        project = self.__db.search('project')
        login = self.__db.search('login')

        advisor_pending_row = advisor_pending.get_row(lambda x: x['ProjectID'] == project_id and x['ID'] == self.__id)
        project_row = project.get_row(lambda x: x['ProjectID'] == project_id)
        login_row = login.get_row(lambda x: x['ID'] == self.__id)
        advisor_pending.update(advisor_pending_row, 'Response_date', date.today())
        while True:
            if respond == 'A':
                advisor_pending.update(advisor_pending_row, 'Response', 'Accept')
                login.update(login_row, 'role', 'advisor')

                if project.table[project_row]['Member1'] == '-':
                    project.update(project_row, 'Member1', f'{self.__id}{self.__first}')
                    break

            elif respond == 'D':
                advisor_pending.update(advisor_pending_row, 'Response', 'Deny')
                break

            else:
                print('Your option is none in above. Please enter your choice again.')
                continue

