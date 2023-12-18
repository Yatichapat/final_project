from database import DB, Table, gen_project_id
from datetime import date
database = DB()


class Faculty:

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

    def view_project_detail(self):
        project = self.__db.search('project')

        for item in project.table:
            print('---------------------------------------')
            print('This is project detail:')
            print(f"ProjectID: {item['ProjectID']}\n Title: {item['Title']}\n Lead: {item['Lead']}\n "
                  f"Member1: {item['Member1']}\n Member2: {item['Member2']}\n Advisor: {item['Advisor']}")

    def check_request_advisor(self):
        project = self.__db.search('project')
        advisor_pending = self.__db.search('advisor_pending')

        advisor_pending_row = advisor_pending.filter(lambda x: x['to_faculty'] == f'{self.__id}_{self.__first}')
        project_advisor = project.join(advisor_pending, 'ProjectID')
        request_to_handle = []
        project_advisor_row = project_advisor.filter(lambda x: x['to_faculty'] == f'{self.__id}_{self.__first}')

        if len(advisor_pending_row.table) > 0:
            print('---------------------------------------')
            print(f'Notification count: {len(advisor_pending_row.table)}.')
            for item in project_advisor_row.table:
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

    def respond_advisor_request(self, project_id, respond):
        advisor_pending = self.__db.search('advisor_pending')
        project = self.__db.search('project')
        login = self.__db.search('login')

        advisor_pending.update('ProjectID', project_id, {'Response_date': date.today()})

        for item in project.table:
            if respond.lower() == 'y':
                advisor_pending.update('ProjectID', project_id, {'Response': 'Accept'})
                login.update('ID', self.__id, {'role': 'advisor'})

                if item['Advisor'] == '-':
                    project.update('ProjectID', project_id, {'Advisor': f'{self.__id}_{self.__first}'})
                    print('You have accept the offer.')
                    self.view_project_detail()
                    break

            elif respond.lower() == 'n':
                advisor_pending.update('ProjectID', project_id, {'Response': 'Deny'})
                print('You have denied the offer.')

            else:
                print('Your option is none in above. Please enter your choice again.')
                respond = input('Do you want to accept offer?: ')

    def respond_committee_request(self, project_id, respond):
        project = self.__db.search('project')

        project_row = project.get_row(lambda x: x['ProjectID'] == project_id)
        for res in project_row.table:
            if respond.lower() == 'y':
                if res['Committee1'] == '-':
                    project.update('Advisor', self.__id, {'Committee1': f'{self.__id}_{self.__first}'})
                elif res['Committee2'] == '-':
                    project.update('Advisor', self.__id, {'Committee2': f'{self.__id}_{self.__first}'})
                elif res['Committee3'] == '-':
                    project.update('Advisor', self.__id, {'Committee3': f'{self.__id}_{self.__first}'})
            elif respond.lower() == 'n':
                print('You have denied the offer.')

            else:
                print("Your answer is unavailable")

    def check_request_evaluate(self):
        project_row = self.__db.search('project').filter(lambda x: x['Status'] == 'Submit')

        for request in project_row.table:
            print(f"ProjectID: {request['ProjectID']}, Title: {request['Title']}, "
                  f"Lead: {request['Lead']}, Member1: {request['Member1']}, Member2: {request['Member2']}")

    def evaluated_project(self, project_id, approve):
        project = self.__db.search('project')
        project_row = project.filter(lambda x: x['ProjectID'] == project_id)
        for res in project_row.table:
            if approve.lower() == 'y':
                if res['Committee1'] == '-':
                    project.update('Advisor', self.__id, {'Committee1': 'Approved'})
                elif res['Committee2'] == '-':
                    project.update('Advisor', self.__id, {'Committee2': 'Approved'})
                elif res['Committee3'] == '-':
                    project.update('Advisor', self.__id, {'Committee3': 'Approved'})
            elif approve.lower() == 'n':
                if res['Committee1'] == '-':
                    project.update('Advisor', self.__id, {'Committee1': 'Unapproved'})
                elif res['Committee2'] == '-':
                    project.update('Advisor', self.__id, {'Committee2': 'Unapproved'})
                elif res['Committee3'] == '-':
                    project.update('Advisor', self.__id, {'Committee3': 'Unapproved'})

            else:
                print("Your answer is unavailable")



class Advisor(Faculty):
    def __init__(self, data_dict, db):
        super().__init__(data_dict, db)
        self.__id = data_dict['ID']
        self.__user = data_dict['user']
        self.__first = data_dict['first']
        self.__last = data_dict['last']
        self.__role = data_dict['role']
        self.__db = db

    def view_detail_project(self):
        project = self.__db.search('project')
        project_row = project.get_row(lambda x: x['Advisor'] == self.__id)
        return project_row

    def approve_project(self, respond):
        project = self.__db.search('project')

        if respond.lower() == 'y':
            project.update('Advisor', self.__id, {'Status': 'Approved'})

        elif respond.lower() == 'n':
            project.update('Advisor', self.__id, {'Status': 'Unapproved'})

        else:
            print("Your answer is unavailable")



