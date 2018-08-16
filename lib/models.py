from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Table,
    Enum)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from datetime import datetime
import enum

Base = declarative_base()
DATABASE = 'todoapp.db'


def set_up_connection(connection_string=None):
    engine = create_engine(f'sqlite:///todoapp.db')
    session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return session()


class TaskUserEditors(Base):
    __tablename__ = 'task_users_editors'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    task_id = Column(Integer, ForeignKey('tasks.id'))


task_folder_association_table = Table(
    'task_folders', Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('folder_id', Integer, ForeignKey('folders.id'))
)


class TaskStatus(enum.Enum):
    CREATED = 'Created'
    TODO = 'Todo'
    INWORK = 'In work'
    DONE = 'Done'
    ARCHIVED = 'Archived'


class TaskPriority(enum.Enum):
    NONE = 'None'
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'


class Folder(Base):
    __tablename__ = 'folders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)

    name = Column(String)
    tasks = relationship('Task', secondary=task_folder_association_table)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __str__(self):
        return self.name


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    parent_task_id = Column(Integer, ForeignKey('tasks.id'), nullable=True)
    assigned_id = Column(Integer, nullable=True)

    name = Column(String)
    description = Column(String)

    priority = Column(Enum(TaskPriority), default=TaskPriority.LOW,
                      nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.CREATED,
                    nullable=False)

    start_date = Column(DateTime)
    end_date = Column(DateTime)

    created = Column(DateTime, nullable=False, default=datetime.now())
    updated = Column(DateTime, nullable=False, default=datetime.now())

    editors = relationship('TaskUserEditors')

    notifications = relationship('Notification', back_populates='task')

    #  uselist prop allows to set one to one relation
    repeat = relationship("Repeat", uselist=False, back_populates='task')

    def __init__(self, name, owner_id, description=None,
                 start_date=None, end_date=None,
                 priority=None, status=None, parent_task_id=None, assigned_id=None):
        self.name = name
        self.owner_id = owner_id
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.parent_task_id = parent_task_id
        self.assigned_id = assigned_id
        self.priority = priority
        self.status = status

    def __str__(self):
        self.created = self.created.strftime('%Y-%m-%d %H:%M')
        self.updated = self.updated.strftime('%Y-%m-%d %H:%M')
        if self.start_date:
            self.start_date = self.start_date.strftime('%Y-%m-%d %H:%M')
        if self.end_date:
            self.end_date = self.end_date.strftime('%Y-%m-%d %H:%M')
        return (
            f'\n'
            f'ID : {self.id}\n'
            f'Owner_id: {self.owner_id}\n'
            f'Parent_task_id: {self.parent_task_id}\n'
            f'Name: {self.name}\n'
            f'Description: {self.description}\n'
            f'Status: {self.status.value}\n'
            f'Priority: {self.priority.value}\n'
            f'Created: {self.created}\n'
            f'Updated: {self.updated}\n'
            f'Start Date: {self.start_date}\n'
            f'End Date: {self.end_date}\n'
        )


class Period(enum.Enum):
    MIN = 'Min'
    HOUR = 'Hour'
    DAY = 'Day'
    WEEK = 'Week'
    MONTH = 'Month'
    YEAR = 'Year'


class EndType(enum.Enum):
    NEVER = 'Never'
    AMOUNT = 'Amount'
    DATE = 'Date'


class Repeat(Base):
    __tablename__ = 'repeats'
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    user_id = Column(Integer)

    task = relationship('Task', back_populates='repeat')

    period = Column(Enum(Period))
    period_amount = Column(Integer)
    end_type = Column(Enum(EndType))
    repetitions_amount = Column(Integer, nullable=False, default=0)
    repetitions_counter = Column(Integer, nullable=False, default=0)
    last_activated = Column(DateTime)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    def __init__(self, user_id, task_id,
                 period, period_amount,
                 end_type,
                 repetitions_amount,
                 end_date, start_date):
        self.user_id = user_id
        self.task_id = task_id
        self.period = period
        self.period_amount = period_amount
        self.end_type = end_type
        self.repetitions_amount = repetitions_amount
        self.end_date = end_date
        self.start_date = start_date
        self.last_activated = self.start_date

    def __str__(self):
        if self.end_date:
            self.end_date = self.end_date.strftime('%Y-%m-%d %H:%M')
        if self.start_date:
            self.start_date = self.start_date.strftime('%Y-%m-%d %H:%M')
        self.last_activated = self.last_activated.strftime('%Y-%m-%d %H:%M')
        return (f'\n'
                f'Owner ID : {self.user_id}\n'
                f'Task ID: {self.task_id}\n'
                f'Period: {self.period.value}\n'
                f'Period amount: {self.period_amount}\n'
                f'End type: {self.end_type.value}\n'
                f'Repetitions_amount: {self.repetitions_amount}\n'
                f'Repetitions count: {self.repetitions_amount}\n'
                f'Start date: {self.start_date}\n'
                f'End date: {self.end_date}\n'
                f'Last activated: {self.last_activated}\n'
                f'')


class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    task = relationship('Task', back_populates='notifications')

    def __init__(self, task, date):
        self.task = task
        self.date = date

    def __str__(self):
        return (
            f'\n'
            f'                ID : {self.id}\n'
            f'                Date: {self.date}\n'
            f'                Task: {self.task_id}\n'
            f'            '
        )
