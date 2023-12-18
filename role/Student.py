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
        login = self.__db.search('login')
        person_login = person.join(login, 'ID')
        print("ID         Firstname   Lastname")
        for item in person_login.table:
            if item['role'] == 'student':
                print(f"{item['ID']:<10} {item['first']:<12}{item['last']:<15}")

    def view_faculty_list(self):
        person = self.__db.search('person')
        login = self.__db.search('login')
        person_login = person.join(login, 'ID')
        print("ID         Firstname   Lastname")
        for item in person_login.table:
            if item['role'] == 'faculty':
                print(f"{item['ID']:<10} {item['first']:<12}{item['last']:<15}")

    def view_project_detail(self):
        project = self.__db.search('project')

        for item in project.table:
            print('---------------------------------------')
            print('This is project detail:')
            print(f"ProjectID: {item['ProjectID']}\n Title: {item['Title']}\n Lead: {item['Lead']}\n "
                  f"Member1: {item['Member1']}\n Member2: {item['Member2']}\n Advisor: {item['Advisor']}")

    def check_request(self):
        project = self.__db.search('project')
        member_pending = self.__db.search('member_pending')

        member_pending_row = member_pending.filter(lambda x: x['to_student'] == f'{self.__id}_{self.__first}')
        project_member = project.join(member_pending, 'ProjectID')
        request_to_handle = []
        project_member_row = project_member.filter(lambda x: x['to_student'] == f'{self.__id}_{self.__first}')

        if len(member_pending_row.table) > 0:
            print('---------------------------------------')
            print(f'Notification count: {len(member_pending_row.table)}.')
            for item in project_member_row.table:
                print(f"ProjectID: {item['ProjectID']}, Title: {item['Title']}, to_be_member: {item['to_be_member']}")
            project_id = str(input("Type Project ID that you want or Type exit to skip the question: "))
            if project_id != 'exit':
                respond = input('Do you want to accept offer?(y/n): ')
                request_to_handle.append((project_id, respond))
                return request_to_handle
        else:
            print('---------------------------------------')
            print("Notification count: 0")
            print("You don't have any notification yet")

    def respond_member_request(self, project_id, respond):
        member_pending = self.__db.search('member_pending')
        project = self.__db.search('project')
        login = self.__db.search('login')

        member_pending.update('ProjectID', project_id, {'Response_date': date.today()})

        for item in project.table:
            if respond.lower() == 'y':
                member_pending.update('ProjectID', project_id, {'Response': 'Accept'})
                login.update('ID', self.__id, {'role': 'member'})

                if item['Member1'] == '-':
                    project.update('ProjectID', project_id, {'Member1': f'{self.__id}_{self.__first}'})
                    print('You have accept the offer.')
                    self.view_project_detail()
                    break
                else:
                    project.update('ProjectID', project_id, {'Member2': f'{self.__id}_{self.__first}'})
                    print('You have accept the offer.')
                    self.view_project_detail()
                    break

            elif respond.lower() == 'n':
                member_pending.update('ProjectID', project_id, {'Response': 'Deny'})
                print('You have denied the offer.')

            else:
                print('Your option is none in above. Please enter your choice again.')
                respond = input('Do you want to accept offer?: ')

    def create_project(self, title):
        project = self.__db.search('project').table
        gen_proj = gen_project_id()
        new_proj = {
            'ProjectID': gen_proj,
            'Title': title,
            'Lead': f'{self.__id}_{self.__first}',
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
                print('Successfully access the lead. This is your Project default setting.\n'
                      '---------------------------------------')

            else:
                print(f"Error: User with ID {self.__id} not found in the login table.")
        for item in project:
            print(f"ProjectID: {item['ProjectID']}\nTitle: {item['Title']}\nLead: {item['Lead']}\n"
                  f"Member1: {item['Member1']}\nMember2: {item['Member2']}\nAdvisor: {item['Advisor']}")


class Lead(Student):
    def __init__(self, data_dict, db):
        super().__init__(data_dict, db)
        self.__id = data_dict['ID']
        self.__user = data_dict['username']
        self.__first = data_dict['first']
        self.__last = data_dict['last']
        self.__role = data_dict['role']
        self.__db = db

    def send_request_member(self, student_id, student_name):
        project = self.__db.search('project')
        project_row = project.filter(lambda x: x['Lead'] == f'{self.__id}_{self.__first}')

        for item in project_row.table:
            if item['Lead'] == f'{self.__id}_{self.__first}':
                project_id = item['ProjectID']

        student_num_request = self.__db.search('student').filter(lambda x: x['ProjectID'] == project_id)
        member_pending = self.__db.search('member_pending').table
        new_mem = {
            'ProjectID': project_id,
            'to_be_member': f'{self.__id}_{self.__first}',
            'Response': '-',
            'Response_date': '-',
            'to_student': f'{student_id}_{student_name}'
        }
        member_pending.append(new_mem)

        num_requests = len(project_row.table)
        for num in student_num_request.table:
            num['num_request'] = num_requests
            print(num['num_request'])
        if member_pending:
            print('----------------------------------------\n'
                  'Your request has now sent')

    def send_request_advisor(self, faculty_id, faculty_name):
        project = self.__db.search('project')
        project_row = project.filter(lambda x: x['Lead'] == f'{self.__id}_{self.__first}')

        for item in project_row.table:
            if item['Lead'] == f'{self.__id}_{self.__first}':
                project_id = item['ProjectID']

        advisor_pending = self.__db.search('advisor_pending').table
        new_mem = {
            'ProjectID': project_id,
            'to_be_member': f'{self.__id}_{self.__first}',
            'Response': '-',
            'Response_date': '-',
            'to_faculty': f'{faculty_id}_{faculty_name}'
        }
        advisor_pending.append(new_mem)
        if advisor_pending:
            print('----------------------------------------\n'
                  'Your request has now sent')

    def auto_reject_request(self):
        member_pending = self.__db.search('member_pending')

        member_pending_row = member_pending.filter(lambda x: x['to_be_member'] == f'{self.__id}_{self.__first}')
        current_date = datetime.now()
        for date_respond in member_pending_row.table:
            response_date_str = member_pending_row['Response_date']
            response_date = datetime.strptime(response_date_str,
                                              '%Y-%m-%d').date() if response_date_str != '-' else None

            if response_date and response_date + timedelta(days=3) <= current_date:
                member_pending.update(member_pending_row, 'Response', 'Deny')

    def check_request_member(self):
        member_pending = self.__db.search('member_pending')

        pending_request = member_pending.filter(lambda x: x['to_be_member'] == f'{self.__id}_{self.__first}')
        if pending_request:
            print('Pending Membership Requests:')
            for request in pending_request.table:
                print(f"ProjectID: {request['ProjectID']}, To: {request['to_student']}, "
                      f"Response: {request['Response']}")
        else:
            print('No Pending Membership Request yet.')

    def check_advisor_request(self):
        advisor_pending = self.__db.search('advisor_pending')

        pending_request = advisor_pending.get_row(lambda x: x['to_be_advisor'] == f'{self.__id}_{self.__first}')
        if pending_request.table:
            print('Pending Advisor Requests:')
            for request in pending_request:
                print(f"ProjectID: {request['ProjectID']}, To: {request['to_advisor']}")
        else:
            print('No pending advisor request found.')

    def submit_project(self):
        project = self.__db.search('project')
        for item in project.table:
            if item['Advisor'] != '-':
                project.update('Lead', f'{self.__id}_{self.__first}', {'Status': 'Submit'})
            else:
                print("You can't submit the project without advisor")



class Member(Student):
    def __init__(self, data_dict, db):
        super().__init__(data_dict, db)
        self.__id = data_dict['ID']
        self.__user = data_dict['username']
        self.__first = data_dict['first']
        self.__last = data_dict['last']
        self.__role = data_dict['role']
        self.__db = db

    def check_request_member(self):
        member_pending = self.__db.search('member_pending')

        pending_request = member_pending.get_row(
            lambda x: x['Member1'] == f'{self.__id}{self.__first}' or x['Member2'] == f'{self.__id}_{self.__first}')

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

