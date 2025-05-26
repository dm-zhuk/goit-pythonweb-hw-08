from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from models import Base, Student, Group, Teacher, Subject, Grade
from faker import Faker
import random

engine = create_engine("postgresql://devops:admin@localhost:5432/student_db")
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def seed_database():
    db: Session = SessionLocal()

    fake = Faker()

    try:
        groups = [Group(name=fake.word()) for _ in range(3)]
        db.add_all(groups)
        db.commit()

        students = []
        for _ in range(30):
            student = Student(name=fake.name(), group=random.choice(groups))
            students.append(student)
        db.add_all(students)
        db.commit()

        teachers = [Teacher(name=fake.name()) for _ in range(5)]
        db.add_all(teachers)
        db.commit()

        subject_names = [
            "Math",
            "Physics",
            "Algorithms",
            "Data Structures",
            "MySQL Database",
            "Java Programming",
            "Python Programming",
            "Computer Science",
        ]
        subjects = [
            Subject(name=name, teacher=random.choice(teachers))
            for name in random.sample(subject_names, 6)
        ]
        db.add_all(subjects)
        db.commit()

        for student in students:
            for _ in range(random.randint(1, 20)):
                grade = Grade(
                    grade=random.randint(1, 100),
                    date_received=fake.date_this_year(),
                    student=student,
                    subject=random.choice(subjects),
                )
                db.add(grade)

        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error occurred: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
