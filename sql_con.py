import bcrypt
import sqlalchemy
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column,Session


sqlite_engine=sqlalchemy.create_engine("sqlite:///test.db")
session=Session(sqlite_engine)


class Base(sqlalchemy.orm.DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    email:Mapped[str]=mapped_column(String(32),primary_key=True)
    username:Mapped[str]=mapped_column(String(32))
    password:Mapped[str]=mapped_column(String(128))


class Question(Base):
    __tablename__ = "questions"
    email:Mapped[str]=mapped_column(String(32))
    question:Mapped[str]=mapped_column(String())
    title:Mapped[str]=mapped_column(String(32))
    qID:Mapped[int]=mapped_column(Integer(),primary_key=True)
    likes:Mapped[int]=mapped_column(Integer())
    dislikes:Mapped[int]=mapped_column(Integer())
    tags:Mapped[str]=mapped_column(String())


class Testcase(Base):
    __tablename__ = "testcases"
    email:Mapped[str]=mapped_column(String(32))
    test_in:Mapped[str]=mapped_column(String())
    test_out:Mapped[str]=mapped_column(String())
    tID:Mapped[int]=mapped_column(Integer(),primary_key=True)
    qID:Mapped[int]=mapped_column(Integer())
    likes:Mapped[int]=mapped_column(Integer())
    dislikes:Mapped[int]=mapped_column(Integer())


class Submission(Base):
    __tablename__ = "submissions"
    email:Mapped[str]=mapped_column(String(32),primary_key=True)
    code:Mapped[str]=mapped_column(String())
    cases_passed:Mapped[int]=mapped_column(Integer())
    total_cases:Mapped[int]=mapped_column(Integer())


def create_user(email:str,username:str,password:str):

    if session.get(User,email) is not None:
        return False

    salt = bcrypt.gensalt(10)
    hashed_pass = bcrypt.hashpw(password.encode("utf-8"), salt).decode()
    user=User(email=email,username=username,password=hashed_pass)
    session.add(user)
    session.commit()
    return True


def login_user(email:str,password:str):
    user=session.query(User).filter(User.email==email).first()
    if not user:
        return False
    else:
        password_check = bcrypt.checkpw(password.encode("utf-8"),user.password.encode("utf-8"))
        if password_check:
            return user
        else:
            return None

def add_question(question:Question):
    session.add(question)
