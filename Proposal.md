## Evaluate the senior student project

- If the leader send the invitation + project's detail to faculty
  - The status of project = 'waiting for evaluation'
- insert project_evaluate new table in database to contain the request for advisor to agreed
- if faculty approved the project
  - The status of project = 'waiting for supervisor to approved'
  - if Supervisor approved the project
    - project['status'] == 'Approved'
- if they denied (at least one of them)
  - The status of project = 'Not approved' and display reason why they denied

Eventually if project have responded from supervisor or getting denied, the project will delete from dictionary from project_evaluate