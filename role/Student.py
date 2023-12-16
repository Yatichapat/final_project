from database import DB, Table, gen_project_id, write_csv
from datetime import date, datetime, timedelta
database = DB()


class Student:
    def __init__(self, data_dict, db):
        self.__id = data_dict['ID']
        self.__user = data_dict['username']
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

    def view_student_list(self):
        if self.__role == 'student':
            print(f"ID: {self.__id} Firstname: {self.__first} Lastname: {self.__last} Role: {self.__role}")

    def respond_member_request(self, project_id, respond):
        member_pending = self.__db.search('member_pending')
        project = self.__db.search('project')
        login = self.__db.search('login')

        member_pending_row = member_pending.get_row(lambda x: x['ProjectID'] == project_id and x['ID'] == self.__id)
        project_row = project.get_row(lambda x: x['ProjectID'] == project_id)
        login_row = login.get_row(lambda x: x['ID'] == self.__id)
        member_pending.update(member_pending_row, 'Response_date', date.today())
        while True:
            if respond.lower() == 'a':
                member_pending.update(member_pending_row, 'Response', 'Accept')
                login.update(login_row, 'role', 'member')

                if project.table[project_row]['Member1'] == '-':
                    project.update(project_row, 'Member1', f'{self.__id}{self.__first}')
                    break
                else:
                    project.update(project_row, 'Member2', f'{self.__id}{self.__first}')
                    break
            elif respond.lower() == 'd':
                member_pending.update(member_pending_row, 'Response', 'Deny')
                break

            else:
                print('Your option is none in above. Please enter your choice again.')
                continue

    def create_project(self, title):
        new_proj = {
            'ProjectID': gen_project_id(),
            'Title': title,
            'Lead': f'{self.__id}{self.__first}',
            'Member1': '-',
            'Member2': '-',
            'Advisor': '-',
            'Status': 'Processing'
        }
        self.__db.search('project').insert(new_proj)

        login = self.__db.search('login')
        login_row = login.get_row(lambda x: x['ID'] == self.__id)
        login.update(login_row, 'role', 'lead')


class Lead(Student):

    def send_request_member(self, project_id, student_name, student_id):
        login = self.__db.search('login')
        member_pending = self.__db.search('member_pending')
        login_row = login.get_row(lambda x: x['ID'] == student_id and x['first'] == student_name and x['role'] == 'student')

        if login_row:
            new_request = {
                'ProjectID': project_id,
                'to_be_member': f'{self.__id}{self.__first}',
                'Response': '-',
                'Response date': date.today()
            }
            member_pending.insert(new_request)

    def auto_reject_request(self):
        member_pending = self.__db.search('member_pending')

        member_pending_row = member_pending.get_row(lambda x: x['ID'] == self.__id)
        current_date = datetime.now()
        for date_respond in member_pending.table:
            if date_respond['Respond_date'] + timedelta(days=3) <= current_date:
                member_pending_row.update(member_pending_row, 'Response', 'Deny')

    def check_request_member(self, project_id):
        member_pending = self.__db.search('member_pending')
        current_date = datetime.now().date()

        pending_request = member_pending.get_row(lambda x: x['Response'] == '-' and x['Response_date'] <= current_date)

        if pending_request:
            print('Pending Membership Requests:')
            for request in pending_request:
                print(f"ProjectID: {request['ProjectID']}, To Be Member: {request['to_be_member']}")
        else:
            print('No pending membership request found.')

    def check_advisor_request(self):
        advisor_pending = self.__db.search('advisor_pending')
        current_date = datetime.now().date()

        pending_request = advisor_pending.get_row(lambda x: x['Response'] == '-' and x['Response_date'] <= current_date)

        if pending_request:
            print('Pending Advisor Requests:')
            for request in pending_request:
                print(f"ProjectID: {request['ProjectID']}, To Be Member: {request['to_be_member']}")
        else:
            print('No pending advisor request found.')


class Member(Student):
    def check_request_member(self):
        member_pending = self.__db.search('member_pending')

        pending_request = member_pending.get_row(
            lambda x: x['Member1'] == f'{self.__id}{self.__first}' or x['Member2'] == f'{self.__id}{self.__first}')

        if pending_request:
            print('Pending Membership Requests:')
            for request in pending_request:
                print(f"ProjectID: {request['ProjectID']}, "
                      f"To Be Member: {request['to_be_member']}, has now accepted the request")
        else:
            print('No pending membership request found.')

    def check_advisor_request(self):
        advisor_pending = self.__db.search('advisor_pending')
        current_date = datetime.now().date()

        pending_request = advisor_pending.get_row(lambda x: x['Response'] == '-' and x['Response_date'] <= current_date)

        if pending_request:
            print('Pending Advisor Requests:')
            for request in pending_request:
                print(f"ProjectID: {request['ProjectID']}, To Be Member: {request['to_be_member']}")
        else:
            print('No pending advisor request found.')