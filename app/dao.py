from app import db
from app.models import Employee, Passbook, ActivityLog

import hashlib


def change_employee_info(employee_id, name, gender, date_of_birth, phone, address):
    employee = Employee.query.get(employee_id)

    employee.name = name
    if gender != '':
        employee.gender = gender
    if date_of_birth != '':
        employee.date_of_birth = date_of_birth
    employee.phone = phone
    if address != "None":
        employee.address = address

    db.session.add(employee)
    db.session.commit()


def change_employee_pass(employee_id, password):
    employee = Employee.query.get(employee_id)

    employee.password = password

    db.session.add(employee)
    db.session.commit()


def set_employee_status(employee_id):
    employee = Employee.query.get(employee_id)

    employee.active = False

    db.session.add(employee)
    db.session.commit()

def get_passbook_list(passbook_id):
    passbooks = Passbook.query

    if passbook_id is not None:
        passbooks = passbooks.filter(Passbook.id.contains(passbook_id))

    return passbooks.all()


def add_activity_log(activity_time, activity, description, employee_id):
    activity_log = ActivityLog(activity_time=activity_time, activity=activity,
                               description=description, employee_id=employee_id)
    db.session.add(activity_log)
    db.session.commit()

    return activity_log
