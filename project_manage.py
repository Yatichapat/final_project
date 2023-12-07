# import database module
import csv
from database import DB, Table, read_csv, write_csv
from role import Student, Admin

# define a function called initializing


def initializing():
    # here are things to do in this function:

    # create an object to read an input csv file, persons.csv
    person = read_csv('persons.csv')
    login = read_csv('login.csv')
    advisor_pending = read_csv('Advisor_pending_request.csv')
    member_pending = read_csv('Member_pending_request.csv')
    project = read_csv('project.csv')

    # create a 'persons' table
    table_person = Table('person', person)
    table_login = Table('login', login)
    table_advisor_pend = Table('advisor_pending', advisor_pending)
    table_member_pend = Table('member_pending', member_pending)
    table_project = Table('project.csv', project)

    # add the 'persons' table into the database
    my_db.insert(table_person)
    my_db.insert(table_login)
    my_db.insert(table_advisor_pend)
    my_db.insert(table_member_pend)
    my_db.insert(table_project)
    print(table_login)


def login():
    username = input('Enter username: ')
    password = input('Enter password: ')
    my_login = my_db.search('login')

    for entry in my_login.table:
        if entry['username'] == username and entry['password'] == password:
            return [entry['ID'], entry['role']]
    return None


# define a function called exit

def exit():
    write_csv('project.csv', 'projects', my_db)



# here are things to do in this function:
   # write out all the tables that have been modified to the corresponding csv files
   # By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:
   
   # https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


# make calls to the initializing and login functions defined above
my_db = DB()
initializing()
val = login()





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
exit()
