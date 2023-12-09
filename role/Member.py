class Member:
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