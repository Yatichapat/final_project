from database import DB, Table, gen_project_id
import Student
from datetime import date
database = DB()


class Leader:
    def __init__(self, data_dict, db):
        self.__id = data_dict['ID']
        self.__user = data_dict['user']
        self.__first = data_dict['first']
        self.__last = data_dict['last']
        self.__role = data_dict['role']
        self.__db = db

    def __str__(self):
        return (f'Hello {self.__user}. You are now activate as a {self.__role}\n'
                f'This is the user information\n'
                f'First name: {self.__first}\n'
                f'Last name: {self.__last}\n'
                f'ID: {self.__id}')

    def send_member_request(self, project_id, request):
        student_list = self.__db.search('student')





    # def respond_member_request(self, project_id, respond):
    #     member_pending = self.__db.search('Member_pending_request')
    #     project = self.__db.search('project')
    #     login = self.__db.search('login')
    #
    #     member_pending_row = member_pending.get_row(lambda x: x['ProjectID'] == project_id and x['ID'] == self.__id)
    #     project_row = project.get_row(lambda x: x['ProjectID'] == project_id)
    #     login_row = login.get_row(lambda x: x['ID'] == self.__id)
    #     member_pending.update(member_pending_row, 'Response_date', date.today())