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
        person = self.__db.search('person')
        print("ID---------Firstname---Lastname-------Role")
        for item in person.table:
            if item['type'] == 'student':
                print(f"{item['ID']:<10} {item['first']:<12}{item['last']:<15}")

    def view_project_detail(self):
        project = self.__db.search('project')
        member_pending = self.__db.search('member_pending')

        project_member = project.join(member_pending, 'ProjectID')
        project_member_filter = project_member.filter(lambda x: x['to_member'] == f'{self.__id}{self.__first}')
        for item in project_member_filter.table:
            print('This is project detail:')
            print(f"ProjectID: {item['ProjectID']}, Title: {item['Title']}, Lead: {item['Lead']}, "
                  f"Member1: {item['Member1']}, Member2: {item['Member2']}, Advisor: {item['Advisor']}")

    def check_request(self):
        # project = self.__db.search('project')
        member_pending = self.__db.search('member_pending').table
        # login = self.__db.search('login')

        member_pending_row = member_pending.filter(lambda x: x['to_member'] == f'{self.__id}{self.__first}')

        if member_pending_row:
            print('You have membership request:')
            for item in member_pending_row:
                print(f"ProjectID: {item['ProjectID']}, to_be_member: {item['to_be_member']}")

            else:
                print("There's no membership request yet.")

    def respond_member_request(self, project_id, respond):
        member_pending = self.__db.search('member_pending')
        project = self.__db.search('project')
        login = self.__db.search('login')

        member_pending_row = member_pending.filter(lambda x: x['ProjectID'] == project_id and x['ID'] == self.__id)
        project_row = project.filter(lambda x: x['ProjectID'] == project_id)
        login_row = login.filter(lambda x: x['ID'] == self.__id)
        member_pending.update(member_pending_row, 'Response_date', date.today())
        while True:
            if respond.lower() == 'a':
                member_pending.update(member_pending_row, 'Response', 'Accept')
                login.update(login_row, 'role', 'member')

                if project.table_info[project_row]['Member1'] == '-':
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
        project = self.__db.search('project').table
        gen_proj = gen_project_id()
        new_proj = {
            'ProjectID': gen_proj,
            'Title': title,
            'Lead': f'{self.__id}{self.__first}',
            'Member1': '-',
            'Member2': '-',
            'Advisor': '-',
            'Status': 'Processing',
            'Committee1': '-',
            'Committee2': '-',
            'Committee3': '-',
            'count_approve': 0
        }
        project.append(new_proj)

        login = self.__db.search('login')
        login_row = login.filter(lambda x: x['ID'] == self.__id)
        for item in login_row.table:
            if item['role'] == 'student':
                item['role'] = 'lead'
                print('Successfully access the lead. This is your Project default setting.')
            else:
                print(f"Error: User with ID {self.__id} not found in the login table.")
        for item in project:
            print(f"ProjectID: {item['ProjectID']}, Title: {item['Title']}, Lead: {item['Lead']}, "
                  f"Member1: {item['Member1']}, Member2: {item['Member2']}, Advisor: {item['Advisor']}")


class Lead(Student):
    def __init__(self, data_dict, db):
        super().__init__(data_dict, db)
        self.__db = db

    def send_request_member(self, student_id, student_name):
        project = self.__db.search('project')
        project_row = project.filter(lambda x: x['Lead'] == f'{self.__id}{self.__first}')

        for item in project_row.table:
            if item['Lead'] == f'{self.__id}{self.__first}':
                project_id = item['ProjectID']

        member_pending = self.__db.search('member_pending')
        new_mem = {
            'ProjectID': project_id,
            'to_be_member': f'{self.__id}{self.__first}',
            'Response': '-',
            'Response_date': '-',
            'to_member': f'{student_id}{student_name}'
        }
        member_pending.append(new_mem)

    def auto_reject_request(self):
        member_pending = self.__db.search('member_pending')

        member_pending_row = member_pending.get_row(lambda x: x['ID'] == self.__id)
        current_date = datetime.now()
        for date_respond in member_pending.table_info:
            if date_respond['Respond_date'] + timedelta(days=3) <= current_date:
                member_pending_row.update(member_pending_row, 'Response', 'Deny')

    def check_request_member(self):
        member_pending = self.__db.search('member_pending')
        current_date = datetime.now().date()

        pending_request = member_pending.filter(lambda x: x['Response'] == '-' and x['Response_date'] <= current_date
                                                          and x['to_be_member'] == f'{self.__id}{self.__first}')

        if pending_request:
            print('Pending Membership Requests:')
            for request in pending_request:
                print(f"ProjectID: {request['ProjectID']}, To Be Member: {request['to_be_member']}, "
                      f"Response: {request['Response']}")
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

