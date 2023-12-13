# import database module
from database import DB, Table, read_csv, write_csv, get_info
from role.Student import Student, Lead, Member
from role.Admin import Admin

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
    table_project = Table('project', project)

    # add the 'persons' table into the database
    my_db.insert(table_person)
    my_db.insert(table_login)
    my_db.insert(table_advisor_pend)
    my_db.insert(table_member_pend)
    my_db.insert(table_project)

    person_join_login = table_person.join(table_login, 'ID')

    # for person_info in person_join_login.table:
    #     admin = Admin(person_info, my_db)
    #     admin.view_all_project()


def login():
    username = input('Enter username: ')
    password = input('Enter password: ')
    my_login = my_db.search('login')

    for entry in my_login.table:
        if entry['username'] == username and entry['password'] == password:
            return [entry['ID'], entry['role']]
    return None


def get_user_data(user_id):
    for person_info in person_join_login:
        if person_info['ID'] == user_id:
            return person_info

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


# based on the return value for login, activate the code that performs activities according to the role defined for that person_id
table_login = my_db.search('login')
table_person = my_db.search('person')
person_join_login = table_person.join(table_login, 'ID').table
print(person_join_login)
while True:
    val = login()
    if val[1] == 'admin':
        person_info = get_user_data(val[0])
        admin = Admin(person_info, my_db)
        print(admin.__str__())
        continue_to_choice = input('Press enter to continue or type exit to log out: ')
        if continue_to_choice.lower() == 'exit':
            print('Successfully log out.')
            continue
        while True:
            print('What do you want to do?')
            print('1. view or modify all user\n'
                  '2. view or modify student user\n'
                  '3. view or modify faculty user\n'
                  '4. view or modify all project\n'
                  '5. view or modify member pending request\n'
                  '6. view or modify advisor pending request\n'
                  '7. reset password for user\n'
                  '8. Invite Faculty for project evaporated')
            choice = int(input('Please select choice: '))
            if choice == 1:
                admin.view_user()
                continue
            elif choice == 2:
                admin.view_all_student()
                modify = input('Press enter 1 to modify or 0 to exit: ')
                if modify == '0':
                    continue
                while True:
                    print()
            elif choice == 3:
                admin.view_all_faculty()

    elif val[1] == 'student':
        person_info = get_user_data(val[0])
        student = Student(person_info, my_db)
        print(student.__str__())
        continue_to_choice = input('Press enter to continue or type exit to log out: ')
        if continue_to_choice.lower() == 'exit':
            print('Successfully log out.')
            continue


    elif val[1] == 'member':
        pass
    elif val[1] == 'lead':
        pass
    elif val[1] == 'faculty':
        pass
    elif val[1] == 'advisor':
        pass


# once everything is done, make a call to the exit function
# exit()
