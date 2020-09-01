from app import db
from app.models import Employee

import hashlib


def employee_change_info(employee_id, name, gender, date_of_birth, phone, address):
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


def employee_change_pass(employee_id, password):
    employee = Employee.query.get(employee_id)

    employee.password = password

    db.session.add(employee)
    db.session.commit()
