import os
import django




# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Student
# Run and print your queries

'''
FC5204	John	Doe	15/05/1995	john.doe@university.com
FE0054	Jane	Smith	null	jane.smith@university.com
FH2014	Alice	Johnson	10/02/1998	alice.johnson@university.com
FH2015	Bob	Wilson	25/11/1996	bob.wilson@university.com

'''

def add_students():
    student_1 = Student(
        student_id = 'FC5204',
        first_name = 'John',
        last_name = 'Doe',
        birth_date='1995-05-15',
        email = 'john.doe@university.com'
    )

    student_2 = Student(
        student_id = 'FE0054',
        first_name = 'Jane',
        last_name = 'Smith',
        email = 'jane.smith@university.com'
    )

    student_3 = Student(
        student_id = 'FH2014',
        first_name = 'Alice',
        last_name = 'Johnson',
        birth_date='1998-02-10',
        email = 'alice.johnson@university.com'
    )

    student_4 = Student(
        student_id = 'FH2015',
        first_name = 'Bob',
        last_name = 'Wilson',
        birth_date='1996-11-25',
        email = 'bob.wilson@university.com'
    )

    Student.objects.bulk_create([student_1, student_2, student_3, student_4])


def get_students_info():
    students = Student.objects.all()
    return '\n'.join(f"Student №{s.student_id}: {s.first_name} {s.last_name}; Email: {s.email}" for s in students)


def update_students_emails():
    students = Student.objects.all()
    for s in students:
        s.email = s.email.replace(s.email.split('@')[1], 'uni-students.com')

    Student.objects.bulk_update(students, ['email'])

update_students_emails()
for student in Student.objects.all():
    print(student.email)

def truncate_students():
    Student.objects.all().delete()