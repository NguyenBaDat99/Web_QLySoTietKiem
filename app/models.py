from sqlalchemy import Column, String, Float, Integer, ForeignKey, Boolean, DateTime, Date, Enum
from sqlalchemy.orm import relationship
from app import db

import datetime
import enum

from flask_login import UserMixin


# class AdminAccount(db.Model, UserMixin):
#     __tablename__ = "admin_account"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)
#     username = Column(String(50), nullable=False)
#     active = Column(Boolean, default=True)
#     password = Column(String(255), nullable=False)
#
#     def __str__(self):
#         return self.username
class EmployeeRole(enum.Enum):
    ADMIN = 1
    EMPLOYEE = 2


class Gender(enum.Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class Position(db.Model):
    __tablename__ = "position"

    id = Column(Integer, primary_key=True, autoincrement=True)
    position_name = Column(String(50), nullable=False)
    employees = relationship('Employee', backref='position', lazy=True)

    def __str__(self):
        return self.position_name


class Employee(db.Model, UserMixin):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False,
                      default="4dff4ea340f0a823f15d3f4f01ab62eae0e5da579ccb851f8db9dfe84c58b2b37b"
                              "89903a740e1ee172da793a6e79d560e5f7f9bd058a12a280433ed6fa46510a")
    name = Column(String(50), nullable=False)
    gender = Column(Enum(Gender), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    phone = Column(String(30), nullable=True)
    address = Column(String(100), nullable=True)
    active = Column(Boolean, nullable=False, default=True)
    employee_role = Column(Enum(EmployeeRole), default=EmployeeRole.EMPLOYEE)
    start_work_date = Column(Date, nullable=True, default=datetime.datetime.utcnow)
    position_id = Column(Integer, ForeignKey(Position.id), nullable=True)
    activity_logs = relationship('ActivityLog', backref='employee', lazy=True)
    transaction_slips = relationship('TransactionSlip', backref='employee', lazy=True)

    def __str__(self):
        return self.username


class ActivityLog(db.Model):
    __tablename__ = "activity_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    activity_time = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    activity = Column(String(50), nullable=False)
    description = Column(String(300), nullable=True)

    def __str__(self):
        return self.id


class Customer(db.Model):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    identity_card_number = Column(Integer, nullable=False)
    phone = Column(String(30), nullable=True)
    passbooks = relationship('Passbook', backref='customer', lazy=True)
    transaction_slips = relationship('TransactionSlip', backref='customer', lazy=True)

    def __str__(self):
        return self.name

    def dump(self):
        return {'id': self.id,
                'name': self.name,
                'identity_card_number': self.identity_card_number,
                'phone': self.phone, }


class PassbookTypes(db.Model):
    __tablename__ = "passbook_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    passbook_type_name = Column(String(50), nullable=False)
    minimum_deposit = Column(Float, nullable=False)
    minimum_deposit_date = Column(Integer, nullable=False)
    interest_rate = Column(Float, nullable=False)
    apply_date = Column(Date, nullable=False, default=datetime.datetime.utcnow)
    term = Column(Integer, nullable=False)
    passbooks = relationship('Passbook', backref='passbook_type', lazy=True)

    def __str__(self):
        return self.passbook_type_name

    def dump(self):
        return {'id': self.id,
                'passbook_type_name': self.passbook_type_name,
                'minimum_deposit': self.minimum_deposit,
                'minimum_deposit_date': self.minimum_deposit_date,
                'interest_rate': self.interest_rate,
                'apply_date': self.apply_date,
                'term': self.term}


class Passbook(db.Model):
    __tablename__ = "passbook"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    passbook_type_id = Column(Integer, ForeignKey(PassbookTypes.id), nullable=False)
    open_date = Column(Date, nullable=False, default=datetime.datetime.utcnow)
    balance_amount = Column(Float, nullable=False)
    transaction_slips = relationship('TransactionSlip', backref='passbook', lazy=True)

    def __str__(self):
        return self.id

    def dump(self):
        return {'id': self.id,
                'customer_id': self.customer_id,
                'passbook_type_id': self.passbook_type_id,
                'open_date': self.open_date,
                'balance_amount': self.balance_amount}


class TransactionSlip(db.Model):
    __tablename__ = "transaction_slip"

    id = Column(Integer, primary_key=True, autoincrement=True)
    passbook_id = Column(Integer, ForeignKey(Passbook.id), nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    employee_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    transaction_date = Column(Date, nullable=False, default=datetime.datetime.utcnow)
    transaction_type = Column(String(20), nullable=False)
    transaction_amount = Column(Float, nullable=False)
    content = Column(String(300), nullable=False)


if __name__ == "__main__":
    db.create_all()
