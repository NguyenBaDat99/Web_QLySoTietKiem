import hashlib
import sqlite3

from sqlalchemy import func, literal, Date, and_

from app import db
from app.models import Employee, Passbook, ActivityLog, Customer, PassbookTypes, TransactionSlip, TransactionType

from datetime import datetime


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


def get_passbook_list(passbook_id=None, customer_id=None, passbook_type_id=None, open_date=None):
    passbooks = Passbook.query

    if passbook_id is not None:
        passbooks = passbooks.filter(Passbook.id.contains(passbook_id))
    elif customer_id is not None:
        passbooks = passbooks.filter(Passbook.customer_id == customer_id)
    elif passbook_type_id is not None:
        passbooks = passbooks.filter(Passbook.passbook_type_id == passbook_type_id)
    elif open_date is not None:
        passbooks = passbooks.filter(Passbook.open_date == open_date)

    return passbooks.all()


def get_passbook(passbook_id):
    passbook = Passbook.query.get(passbook_id)

    return passbook


def find_passbook(passbook_id):
    passbooks = Passbook.query
    passbook_list = passbooks.all()

    for p in passbook_list:
        pID = hashlib.sha512(str(p.id).strip().encode("utf-8")).hexdigest()
        if pID == passbook_id:
            return p

    return None


def add_activity_log(activity, description, employee_id):
    activity_log = ActivityLog()

    activity_log.activity = activity
    activity_log.description = description
    activity_log.employee_id = employee_id

    db.session.add(activity_log)
    db.session.commit()

    return activity_log


def add_transaction_slip(passbook_id, customer_id, employee_id, transaction_type,
                         collect_amount=None, spend_amount=None, interest_amount=None, content=None):
    transaction = TransactionSlip()

    transaction.passbook_id = passbook_id
    transaction.customer_id = customer_id
    transaction.employee_id = employee_id
    transaction.transaction_type = transaction_type

    if collect_amount is not None:
        transaction.collect_amount = collect_amount
    if spend_amount is not None:
        transaction.spend_amount = spend_amount
    if interest_amount is not None:
        transaction.interest_amount = interest_amount
    if content is not None:
        transaction.content = content

    db.session.add(transaction)
    db.session.commit()

    return transaction


def get_passbook_type(passbook_type_id=None, passbook_type_name=None):
    passbook_type = PassbookTypes.query

    if passbook_type_id is not None:
        passbook_type = passbook_type.filter(PassbookTypes.id.contains(passbook_type_id))
    if passbook_type_name is not None:
        passbook_type = passbook_type.filter(PassbookTypes.passbook_type_name.contains(passbook_type_name))

    return passbook_type.all()


def create_passbook(customer_id, passbook_type_id, balance_amount):
    passbook = Passbook(customer_id=customer_id,
                        passbook_type_id=passbook_type_id,
                        balance_amount=balance_amount)

    db.session.add(passbook)
    db.session.commit()

    return passbook


def update_passbook(passbook_id, passbook_type_id=None, balance_amount=None):
    passbook = Passbook.query.get(passbook_id)

    if passbook_type_id is not None:
        passbook.passbook_type_id = passbook_type_id
        passbook.open_date = datetime.now()
    if balance_amount is not None:
        if int(balance_amount) > 0:
            passbook.balance_amount = float(balance_amount)
        else:
            passbook.balance_amount = balance_amount

    db.session.add(passbook)
    db.session.commit()

    return passbook


def create_customer(name, identity_card_number, phone):
    customer = Customer()

    customer.name = name
    customer.identity_card_number = identity_card_number
    if phone != '':
        customer.phone = phone

    db.session.add(customer)
    db.session.commit()

    return customer


def update_customer(customer_id, phone=None):
    customer = Customer.query.get(customer_id)

    if phone is not None:
        customer.phone = phone

    db.session.add(customer)
    db.session.commit()

    return customer


def get_customer_by_id(customer_id):
    customer = Customer.query.get(customer_id)

    return customer


def find_customer(customer_id=None, identity_number=None, name=None):
    customer = Customer.query

    if customer_id is not None:
        customer = customer.filter(Customer.id.contains(customer_id))
    elif identity_number is not None:
        customer = customer.filter(Customer.identity_card_number.contains(identity_number))
    elif name is not None:
        customer = customer.filter(Customer.name.contains(name))

    return customer.all()


def get_transaction_slip(transaction_id=None, passbook_id=None, customer_id=None, employee_id=None,
                         transaction_type=None):
    transaction_slips = TransactionSlip.query

    if transaction_id is not None:
        transaction_slips = transaction_slips.filter(TransactionSlip.id == transaction_id)
    if passbook_id is not None:
        transaction_slips = transaction_slips.filter(TransactionSlip.passbook_id == passbook_id)
    if customer_id is not None:
        transaction_slips = transaction_slips.filter(TransactionSlip.customer_id == customer_id)
    if employee_id is not None:
        transaction_slips = transaction_slips.filter(TransactionSlip.employee_id == employee_id)
    if transaction_type is not None:
        transaction_slips = transaction_slips.filter(TransactionSlip.transaction_type == transaction_type)

    return transaction_slips.all()


def get_transaction_slip_by_date(date):
    from_date = date + ' 00:00:00'
    to_date = date + ' 23:59:59'

    transaction_slips = TransactionSlip.query
    transaction_slips = transaction_slips.filter(TransactionSlip.transaction_date.between(from_date, to_date))

    return transaction_slips


def get_last_transaction_date(passbook_id):
    transaction_slips = TransactionSlip.query
    transaction_slips = transaction_slips.all()

    transaction_date = None

    for p in transaction_slips:
        if p.passbook_id == passbook_id:
            if p.transaction_type == TransactionType.MATURITY:
                transaction_date = p.transaction_date
            elif p.interest_amount != 0:
                transaction_date = p.transaction_date

    return transaction_date


def get_maturity_time(passbook_id, open_date):
    transaction_slips = TransactionSlip.query
    transaction_slips = transaction_slips.all()

    maturity_times = 1

    for p in transaction_slips:
        if p.passbook_id == passbook_id and \
                p.transaction_date > open_date and \
                p.spend_amount == 0:
            maturity_times += 1

    return maturity_times


def report_revenue_day(date):
    from_date = date + ' 00:00:00'
    to_date = date + ' 23:59:59'

    result = db.session.query(
        PassbookTypes.passbook_type_name.label('passbook_type_name'),
        func.sum(TransactionSlip.collect_amount).label('collect_amount'),
        func.sum(TransactionSlip.spend_amount).label('spend_amount'),
        func.sum(TransactionSlip.interest_amount).label('interest_amount'), ) \
        .join(Passbook,
              Passbook.passbook_type_id == PassbookTypes.id) \
        .join(TransactionSlip,
              TransactionSlip.passbook_id == Passbook.id) \
        .filter(TransactionSlip.transaction_date.between(from_date, to_date)) \
        .group_by(PassbookTypes.passbook_type_name) \
        .all()

    return result


def report_passbook_type(date):
    from_date = date + ' 00:00:00'
    to_date = date + ' 23:59:59'

    result = db.session.query(
        Passbook.id,
        PassbookTypes.passbook_type_name,
        PassbookTypes.interest_rate,
        PassbookTypes.term) \
        .join(PassbookTypes,
              PassbookTypes.id == Passbook.passbook_type_id) \
        .join(TransactionSlip,
              TransactionSlip.passbook_id == Passbook.id) \
        .filter(TransactionSlip.transaction_date.between(from_date, to_date)) \
        .group_by(Passbook.id) \
        .all()
    return result


def report_open_close_passbook_month(passbook_type, from_month, to_month):
    from_month = from_month + ' 00:00:00'
    to_month = to_month + ' 00:00:00'

    result = db.session.query(
        TransactionSlip.transaction_date.cast(Date).label('transaction_date'),
        func.COUNT(func.IF(TransactionSlip.transaction_type == TransactionType.OPEN_PASSBOOK, 1, None))
            .label('passbook_open'),
        func.COUNT(func.IF(and_(TransactionSlip.transaction_type == TransactionType.WITHDRAW,
                                Passbook.balance_amount == 0), 1, None))
            .label('passbook_close'), ) \
        .join(Passbook,
              Passbook.id == TransactionSlip.passbook_id) \
        .join(PassbookTypes,
              PassbookTypes.id == Passbook.passbook_type_id) \
        .filter(PassbookTypes.id == passbook_type) \
        .filter(TransactionSlip.transaction_date.between(from_month, to_month)) \
        .group_by(TransactionSlip.transaction_date.cast(Date)) \
        .all()

    return result


def report_open_passbook_month(passbook_type, from_month, to_month):
    from_month = from_month + ' 00:00:00'
    to_month = to_month + ' 00:00:00'

    result = db.session.query(
        Passbook.id,
        Passbook.customer_id,
        Passbook.open_date,
        Passbook.balance_amount)\
        .join(TransactionSlip,
              TransactionSlip.passbook_id == Passbook.id)\
        .join(PassbookTypes,
              PassbookTypes.id == Passbook.passbook_type_id)\
        .filter(PassbookTypes.id == passbook_type)\
        .filter(TransactionSlip.transaction_date.between(from_month, to_month))\
        .filter(TransactionSlip.transaction_type == TransactionType.OPEN_PASSBOOK)\
        .all()

    return result


def report_close_passbook_month(passbook_type, from_month, to_month):
    from_month = from_month + ' 00:00:00'
    to_month = to_month + ' 00:00:00'

    result = db.session.query(
        Passbook.id,
        Passbook.customer_id,
        Passbook.open_date,)\
        .join(TransactionSlip,
              TransactionSlip.passbook_id == Passbook.id)\
        .join(PassbookTypes,
              PassbookTypes.id == Passbook.passbook_type_id)\
        .filter(PassbookTypes.id == passbook_type)\
        .filter(TransactionSlip.transaction_date.between(from_month, to_month))\
        .filter(TransactionSlip.transaction_type == TransactionType.WITHDRAW)\
        .filter(Passbook.balance_amount == 0) \
        .all()

    return result
