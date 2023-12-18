# Final Project

Simulate the senior project to track the work

## Running or Compiling the Python Script

Follow these steps to run or compile your Python script using PyCharm:

### Step 1: Open My final project in PyCharm

### Step 2: Open my project_manage.py File

### Step 3: Run the File

- Right-click on the file.
- Choose "Run <project_manage>" from the context menu.

   Alternatively, you can use the keyboard shortcut:

   - Select the file by clicking on it.
   - Press `Shift + F10` to run the file.
   - Or open the terminal and type "python project_manage.py"

# My process

| Role  | Action                                  | Method               | Class            | Complete Percentage |
|-------|-----------------------------------------|----------------------|------------------|---------------------|
| Admin | Reset password                          | update               | Admin            | 40%                 |
| Admin | Modify user                             | update and remove    | Admin            | 50%                 |
| Admin | Create table                            | insert               | Admin            | 40%                 |
| Admin | Request a committee to evaluate project | update               | Admin            | 60%                 |
| Admin | Delete table                            | remove               | Admin            | 30%                 |
| Student | Create Project                          | append               | Student          | 100%                |
| Student | Check notification                      | join, filter, append | Student          | 100%                |
| Student | Respond offer                           | update               | Student          | 100%                |
| Student | Delete Project                          | filter and remove    | Student          | 30%                 |
| Lead  | Send request member                     | filter and append    | Lead(Student)    | 100%                |
| Lead  | Send request advisor                    | filter and append    | Lead(Student)    | 100%                |
| Lead  | Check pending request                   | filter               | Lead(Student)    | 100%                |
| Lead  | View project detail and status          | filter               | Student          | 100%                |
| Lead  | Submit project to Advisor               | filter and append    | Lead(Student)    | 50%                 |
| Member | Check pending request                   | filter               | Member(Student)  | 80%                 |
| Member | View project detail and status          | filter               | Student          | 90%                 |
| Faculty | Check Notification                      | join, filter, append | Faculty          | 100%                |
| Faculty | Evaluate Project                        | filter, update       | Faculty          | 60%                 |
| Faculty | Respond offer to be advisor             | filter, update       | Faculty          | 20%                 |
| Advisor | Approved project                        | filter, update       | Advisor(Faculty) | 80%                 | 

## Outstanding Issues

### Missing Features

- **Modify Project:** Didn't put the modify features if user wants to edit data in their project.
- **Delete Project:** Didn't put delete function on lead role. (They had to send request to Admin to confirm delete project.)
- **Exit function:** Didn't put exit function when the process had finished.

## Actions for [Admin]

### Bugs and lost features for [Admin]

#### can't create project
#### can't delete table
#### can't insert table
#### can't send request to faculty to be committee

- **can't create project:** Couldn't use insert method for add more table.
- **can't delete table:** Couldn't use a remove method to delete table, so I couldn't confirm delete project for user as well.

#### [Faculty] Bug and lost features

- **can't accept offer to be advisor** When I type 'y' to accept offer it still doesn't end loop and still asked to accept offer or not. 

