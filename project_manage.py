# import database module
from database import DB, Table, read_csv, get_info
from role.Student import Student, Lead, Member
from role.Faculty import Faculty, Advisor
from role.Admin import Admin

# define a function called initializing


def initializing():

    person = read_csv('persons.csv')
    login = read_csv('login.csv')
    advisor_pending = read_csv('Advisor_pending_request.csv')
    member_pending = read_csv('Member_pending_request.csv')
    project = read_csv('project.csv')

    #read role csv
    students = read_csv('Student.csv')
    faculty = read_csv('Faculty.csv')
    admin = read_csv('Admin.csv')

    # create table
    table_person = Table('person', person)
    table_login = Table('login', login)
    table_advisor_pend = Table('advisor_pending', advisor_pending)
    table_member_pend = Table('member_pending', member_pending)
    table_project = Table('project', project)

    # create role table
    admin_table = Table('admin', admin)
    faculty_table = Table('faculty', faculty)
    student_table = Table('student', students)

    # add the 'persons' table into the database
    my_db.insert(table_person)
    my_db.insert(table_login)
    my_db.insert(table_advisor_pend)
    my_db.insert(table_member_pend)
    my_db.insert(table_project)

    my_db.insert(admin_table)
    my_db.insert(faculty_table)
    my_db.insert(student_table)


def login():
    username = input('Enter username: ')
    password = input('Enter password: ')
    my_login = my_db.search('login')

    for entry in my_login.table:
        if entry['username'] == username and entry['password'] == password:
            return [entry['ID'], entry['role']]
    return None

# define a function called exit

# def exit():
#     write_csv('project.csv', 'projects', my_db)



# here are things to do in this function:
   # write out all the tables that have been modified to the corresponding csv files
   # By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:
   
   # https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


# make calls to the initializing and login functions defined above
my_db = DB()
initializing()


# based on the return value for login, activate the code that performs activities according to the role defined for that person_id


while True:
    table_login = my_db.search('login')
    table_person = my_db.search('person')
    person_join_login = table_person.join(table_login, 'ID')
    print(person_join_login)
    val = login()
    person_info = get_info(my_db, val[0])
    if val[1] == 'admin':
        admin = Admin(person_info, my_db)
        print(admin.__str__())
        continue_to_choice = input('Press enter to continue or type exit to log out: ')
        if continue_to_choice.lower() == 'exit':
            print('Successfully log out.')
            continue
        while True:
            print('What do you want to do?')
            print('0. Log out\n'
                  '1. modify all user\n'
                  '2. view request\n'
                  '3. Invite Faculty to be Committee\n')
            choice = int(input('Please select number: '))
            if choice == 0:
                break
            if choice == 1:
                admin.view_user()
                continue
            elif choice == 2:
                admin.reset_password(val[1])
            elif choice == 3:
                project_id = str(input('Enter Project ID: '))
                advisor_id = str(input('Enter Advisor ID: '))
                advisor_name = input('Enter Advisor name: ')
                admin.send_request_committee(project_id, advisor_id, advisor_name)

    elif val[1] == 'student':
        student = Student(person_info, my_db)
        print(student.__str__())
        continue_to_choice = input('Press enter to continue or type exit to log out: ')
        if continue_to_choice.lower() == 'exit':
            print('Successfully log out.')
            continue
        while True:
            print('What do you want to do?')
            print('0. Log out\n'
                  '1. Create Project\n'
                  '2. View notification\n')
            choice = int(input('Please select number: '))
            if choice == 1 and val[1] != ['member']:
                title = input('Enter Title: ')
                student.create_project(title)
                print('Please Log in again to continue as lead')

                break
            elif choice == 2 and val[1] != ['lead']:
                # view project detail
                project_id = str(input('Type Project ID that you want: '))
                respond = input('Do you want to accept offer?')
                student.respond_member_request(project_id, respond)

    elif val[1] == 'member':
        member = Member(person_info, my_db)
        print(member.__str__())
        continue_to_choice = input('Press enter to continue or type exit to log out: ')
        if continue_to_choice.lower() == 'exit':
            print('Successfully log out.')
            continue
        while True:
            print('What do you want to do?')
            print('0. Log out\n'
                  '1. Modify Project\n'
                  '2. Check Member pending request\n'
                  '3. Check Advisor pending request\n'
                  '4. Check Project detail\n')
            choice = int(input('Please select number: '))
            if choice == 1:
                pass
            elif choice == 2:
                member.check_request_member()
            elif choice == 3:
                member.check_advisor_request()
            elif choice == 4:
                pass

    elif val[1] == 'lead':
        lead = Lead(person_info, my_db)
        print(lead.__str__())
        continue_to_choice = input('Press enter to continue or type exit to log out: ')
        if continue_to_choice.lower() == 'exit':
            print('Successfully log out.')
            continue
        while True:
            print('What do you want to do?')
            print('0. Log out\n'
                  '1. Send invitation to Member\n'
                  '2. Check Member pending request\n'
                  '3. Send invitation to Advisor\n'
                  '4. Check Advisor pending request\n')
            choice = int(input('Please select number: '))
            if choice == 1:
                member_id = input('Enter member ID: ')
                member_name = input('Enter member name: ')
                lead.send_request_member(member_id, member_name)
                lead.auto_reject_request()
                continue

            elif choice == 2:
                lead.check_request_member()

    elif val[1] == 'faculty':
        faculty = Faculty(person_info, my_db)
        print(faculty.__str__())
        continue_to_choice = input('Press enter to continue or type exit to log out: ')
        if continue_to_choice.lower() == 'exit':
            print('Successfully log out.')
            continue
        print('What do you want to do?')
        print('0. Log out\n'
              '1. Check notification\n'
              '2. Evaluating projects\n')
        choice = int(input('Please select number: '))
        # if choice == 1:
            # num_request =




    elif val[1] == 'advisor':
        advisor = Advisor(person_info, my_db)
        print(advisor.__str__())
        continue_to_choice = input('Press enter to continue or type exit to log out: ')
        if continue_to_choice.lower() == 'exit':
            print('Successfully log out.')
            continue

# once everything is done, make a call to the exit function
# exit()
