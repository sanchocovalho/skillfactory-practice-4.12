import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DB_PATH = "sqlite:///todos.sqlite3"

Base = declarative_base()

class TodoItem(Base):
    __tablename__ = 'todos_table'

    uid = sa.Column(sa.INTEGER, primary_key=True)
    description = sa.Column(sa.TEXT)
    is_completed = sa.Column(sa.INTEGER, default=0)

def create_session():
    engine = sa.create_engine(DB_PATH)
    
    metadata = sa.MetaData()
    todos_table = sa.Table(
        'todos_table',
        metadata,
        sa.Column('uid', sa.INTEGER, primary_key=True, autoincrement=False),
        sa.Column('description', sa.TEXT),
        sa.Column('is_completed', sa.INTEGER, default=0))
    
    metadata.create_all(engine)
    Sessions = sessionmaker(engine)
    return Sessions()

def get_task_by_id(session, uid):
    return session.query(TodoItem).filter(TodoItem.uid == uid).all()

def make_task_completed(session, uid, is_completed):
    task = get_task_by_id(session, uid)
    task[0].is_completed = int(is_completed)
    session.commit()

def task_to_dict(task):
    return {'uid': task.uid,
            'description': task.description.capitalize(),
            'is_completed': task.is_completed}

def get_all_tasks(session):
    return session.query(TodoItem).all()

def add_task(session, uid, description):
    task = TodoItem(uid=uid, description=description)
    session.add(task)
    session.commit()

def delete_task(session, uid):
    task = get_task_by_id(session, uid)
    session.delete(task[0])
    session.commit()

def get_uncompleted_tasks(session):
    query = session.query(TodoItem).filter(TodoItem.is_completed == '0').count()
    return query
