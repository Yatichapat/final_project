# import database module
import csv
import random
import string
from database import DB, Table


# define a function called initializing

def initializing():
    # here are things to do in this function:

    # create an object to read an input csv file, persons.csv
    person_db = DB()
    person = person_db.read_csv('persons.csv')

    # create a 'persons' table
    table_person = Table('person', person)

    # add the 'persons' table into the database
    person_db.insert(table_person)
    my_table_person = person_db.search('person')

    # create a 'login' table
    table_login = Table('login', [])

    # the 'login' table has the following keys (attributes):
    # person_id
    # username
    # password
    # role

    # a person_id is the same as that in the 'persons' table
    if my_table_person:
        for person in table_person.table:
            person_id = person['ID']

            # let a username be a person's first name followed by a dot and the first letter of that person's last name
            username = f"{person['first']}.{person['last'][0]}"

            # let a password be a random four digits string
            password = ''.join(random.choices(string.digits, k=4))

            # let the initial role of all the students be Member
            # let the initial role of all the faculties be Faculty
            role = 'Member' if person['type'] == 'student' else 'Faculty'

            # create a login table by performing a series of insert operations; each insert adds a dictionary to a list
            login_entry = {
                'ID': person_id,
                'username': username,
                'password': password,
                'role': role
            }
            table_login.insert(login_entry)

    # add the 'login' table into the database
    person_db.insert(table_login)
    print(table_login)
    return table_login


# define a function called login

def login(table_login):
    username = input('Enter username: ')
    password = input('Enter password: ')

    for entry in table_login.table:
        if entry['username'] == username and entry['password'] == password:
            return [entry['ID'], entry['role']]
    return None


# define a function called exit
def exit():
    with open('persons.csv', 'w') as new_person_file:
        fieldnames = ['ID', 'username', 'password', 'role']
        writer = csv.DictWriter(new_person_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(login_table.table)


# here are things to do in this function:
   # write out all the tables that have been modified to the corresponding csv files
   # By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:
   
   # https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


# make calls to the initializing and login functions defined above

login_table = initializing()
val = login(login_table)
print(val)


# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

# if val[1] = 'admin':
    # see and do admin related activities
# elif val[1] = 'student':
    # see and do student related activities
# elif val[1] = 'member':
    # see and do member related activities
# elif val[1] = 'lead':
    # see and do lead related activities
# elif val[1] = 'faculty':
    # see and do faculty related activities
# elif val[1] = 'advisor':
    # see and do advisor related activities


# once everything is done, make a call to the exit function
# exit()
