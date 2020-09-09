from app import db
from app.models import Employee, Passbook, ActivityLog, Customer, PassbookTypes, TransactionSlip


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
        passbooks = passbooks.filter(Passbook.passbook_type_id == passbook_id)
    elif open_date is not None:
        passbooks = passbooks.filter(Passbook.open_date == open_date)

    return passbooks.all()


def add_activity_log(activity_time, activity, description, employee_id):
    activity_log = ActivityLog(activity_time=activity_time, activity=activity,
                               description=description, employee_id=employee_id)
    db.session.add(activity_log)
    db.session.commit()

    return activity_log


def get_passbook_type(passbook_type_id=None):
    passbook_type = PassbookTypes.query

    if passbook_type_id is not None:
        passbook_type = passbook_type.filter(PassbookTypes.id.contains(passbook_type_id))

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
    if balance_amount is not None:
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


def find_customer_by_id(customer_id):
    customer = Customer.query.get(customer_id)

    return customer


def find_customer(customer_id=None, identity_number=None, name=None):
    customer = Customer.query

    if customer_id is not None:
        customer = customer.filter(Customer.id == customer_id)
    elif identity_number is not None:
        customer = customer.filter(Customer.identity_card_number == identity_number)
    elif name is not None:
        customer = customer.filter(Customer.name.contains(name))

    return customer.all()


def create_transaction_slip(passbook_id, customer_id, employee_id,
                            transaction_date, transaction_type, transaction_amount, content=None):
    transaction = TransactionSlip()

    transaction.passbook_id = passbook_id
    transaction.customer_id = customer_id
    transaction.employee_id = employee_id
    transaction.transaction_date = transaction_date
    transaction.transaction_type = transaction_type
    transaction.transaction_amount = transaction_amount
    if content is not None:
        transaction.content = content

    db.session.add(transaction)
    db.session.commit()

    return transaction


