from sqlalchemy import func
from seed import SessionLocal
from models import Group, Student, Teacher, Subject, Grade


# 1. Top 5 students by average grade
def select_1():
    with SessionLocal() as db:
        return (
            db.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
            .join(Grade, Grade.student_id == Student.id)
            .group_by(Student.id, Student.name)
            .order_by(func.avg(Grade.grade).desc())
            .limit(5)
            .all()
        )


# 2. Top student in a specific subject
def select_2(subject_name):
    with SessionLocal() as db:
        return (
            db.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Subject.name == subject_name)
            .group_by(Student.id, Student.name)
            .order_by(func.avg(Grade.grade).desc())
            .limit(1)
            .all()
        )


# 3. Average grades by group for a specific subject
def select_3(subject_name):
    with SessionLocal() as db:
        return (
            db.query(Group.name, func.avg(Grade.grade).label("avg_grade"))
            .select_from(Group)
            .join(Student, Student.group_id == Group.id)
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Subject.name == subject_name)
            .group_by(Group.name)
            .order_by(func.avg(Grade.grade).desc())
            .all()
        )


# 4. Overall average grade in the database
def select_4():
    with SessionLocal() as db:
        result = db.query(func.avg(Grade.grade)).scalar()
        return result if result is not None else 0


# 5. Subjects taught by a specific Teacher
def select_5(teacher_name):
    with SessionLocal() as db:
        return (
            db.query(Subject.name)
            .join(Teacher, Teacher.id == Subject.teacher_id)
            .filter(Teacher.name == teacher_name)
            .all()
        )


# 6. Students in a specific group
def select_6(group_name):
    with SessionLocal() as db:
        return (
            db.query(Student.name)
            .join(Group, Group.id == Student.group_id)
            .filter(Group.name == group_name)
            .all()
        )


# 7. Grades of students in a specific group for a specific subject
def select_7(group_name, subject_name):
    with SessionLocal() as db:
        return (
            db.query(Student.name, Grade.grade)
            .select_from(Group)
            .join(Student, Student.group_id == Group.id)
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Group.name == group_name, Subject.name == subject_name)
            .all()
        )


# 8. Average grade given by a specific Teacher
def select_8(teacher_name):
    with SessionLocal() as db:
        result = (
            db.query(func.avg(Grade.grade))
            .select_from(Teacher)
            .join(Subject, Subject.teacher_id == Teacher.id)
            .join(Grade, Grade.subject_id == Subject.id)
            .filter(Teacher.name == teacher_name)
            .scalar()
        )
        return result if result is not None else 0


# 9. Subjects taken by a specific student
def select_9(student_name):
    with SessionLocal() as db:
        return (
            db.query(Subject.name)
            .select_from(Student)
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Student.name == student_name)
            .distinct()
            .all()
        )


# 10. Subjects taught by a specific Teacher to a specific student
def select_10(teacher_name, student_name):
    with SessionLocal() as db:
        return (
            db.query(Subject.name)
            .select_from(Student)
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .join(Teacher, Teacher.id == Subject.teacher_id)
            .filter(Student.name == student_name, Teacher.name == teacher_name)
            .distinct()
            .all()
        )


if __name__ == "__main__":
    # Fetch test data
    with SessionLocal() as db:
        select_1_data = select_1()  # Top 5 students
        select_5_data = db.query(Teacher.name).all()  # All teachers
        select_6_data = db.query(Group.name).all()  # All groups

    # Run all 10 queries
    print(
        "1. Top 5 students by average grade:",
        [(name, float(avg_grade)) for name, avg_grade in select_1()],
    )
    print(
        "2. Top student in Math:",
        [(name, float(avg_grade)) for name, avg_grade in select_2("Math")],
    )
    print(
        "3. Average grades by group for Math:",
        [(name, float(avg_grade)) for name, avg_grade in select_3("Math")],
    )
    print("4. Overall average grade:", float(select_4()))

    if select_5_data:
        print("5. Subjects taught by first teacher:", select_5(select_5_data[0][0]))
    if select_6_data:
        print("6. Students in first group:", select_6(select_6_data[0][0]))
    if select_6_data and select_5_data:
        print(
            "7. Grades in first group for Math:", select_7(select_6_data[0][0], "Math")
        )
        print(
            "8. Average grade by first teacher:", float(select_8(select_5_data[0][0]))
        )
        print("9. Subjects taken by first student:", select_9(select_1_data[0][0]))
        print(
            "10. Subjects taught by first teacher to first student:",
            select_10(select_5_data[0][0], select_1_data[0][0]),
        )
