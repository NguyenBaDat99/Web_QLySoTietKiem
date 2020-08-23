from sqlalchemy import Column, String, Float, Integer, ForeignKey, Boolean, DateTime, Date
from sqlalchemy.orm import relationship
from app import db, admin
from flask import redirect
import datetime

from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose

from flask_login import UserMixin
from flask_login import current_user
from flask_login import logout_user


class AdminAccount(db.Model, UserMixin):
    __tablename__ = "admin_account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)

    def __str__(self):
        return self.username


class Position(db.Model):
    __tablename__ = "position"

    id = Column(Integer, primary_key=True, autoincrement=True)
    position_name = Column(String(50), nullable=False)
    employees = relationship('Employee', backref='position', lazy=True)

    def __str__(self):
        return self.position_name


class Employee(db.Model):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False, default="c4ca4238a0b923820dcc509a6f75849b")
    name = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    phone = Column(String(30), nullable=True)
    address = Column(String(100), nullable=True)
    start_work_date = Column(Date, nullable=False)
    position_id = Column(Integer, ForeignKey(Position.id), nullable=False)
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
    gender = Column(String(10), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    phone = Column(String(30), nullable=True)
    address = Column(String(100), nullable=True)
    passbooks = relationship('Passbook', backref='customer', lazy=True)
    transaction_slips = relationship('TransactionSlip', backref='customer', lazy=True)

    def __str__(self):
        return self.name


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


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AboutUsView(AuthenticatedBaseView):
    @expose("/")
    def index(self):
        return self.render("admin/about-us.html")


class LogoutView(AuthenticatedBaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")


class PositionModelView(AuthenticatedModelView):
    column_display_pk = True
    can_export = True
    form_columns = ('position_name', )
    form_filters = ('position_name', )


class EmployeeModelView(AuthenticatedModelView):
    column_display_pk = True
    can_export = True
    show_column = 'name', 'username', 'gender', 'date_of_birth', 'phone', 'address', 'start_work_date', 'position',
    form_columns = show_column
    column_filters = show_column
    column_list = show_column


class ActivityLogModelView(AuthenticatedModelView):
    column_display_pk = True
    can_export = True
    can_create = False
    can_delete = False
    can_edit = False
    column_filters = ('activity_time', 'activity', 'employee_id')


class PassbookTypesModelView(AuthenticatedModelView):
    can_export = True
    can_edit = False
    can_delete = False
    show_column = 'passbook_type_name', 'minimum_deposit', 'minimum_deposit_date', 'interest_rate', 'apply_date', 'term',
    column_filters = show_column
    form_columns = show_column


admin.add_view(PositionModelView(Position, db.session))
admin.add_view(EmployeeModelView(Employee, db.session))
admin.add_view(ActivityLogModelView(ActivityLog, db.session))
admin.add_view(PassbookTypesModelView(PassbookTypes, db.session))
# admin.add_view(AboutUsView(name="About us"))
admin.add_view(LogoutView(name="Logout"))


if __name__ == "__main__":
    db.create_all()
