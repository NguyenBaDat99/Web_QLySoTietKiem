from app import app, decorator, dao, models
from flask import request, jsonify
from flask_login import logout_user, current_user
import json

from app.models import TransactionType


@app.route("/api/logout-employee-auto/<int:employee_id>", methods=["post"])
def logout_employee_auto(employee_id):
    if dao.add_activity_log(activity="Đăng xuất tự động",
                            description="Nhân viên không có hoạt động",
                            employee_id=current_user.id):
        logout_user()
        return jsonify({"status": 200})

    return jsonify({"status": 500, "error_message": "Something Wrong!!!"})


@app.route("/api/create-passbook", methods=["post"])
@decorator.login_required_user
def create_passbook():
    try:
        data = json.loads(request.data)
        customer_id = data.get('customer_id')
        passbook_type_id = data.get('passbook_type_id')
        balance_amount = data.get('balance_amount')

        passbook = dao.create_passbook(customer_id=customer_id,
                                       passbook_type_id=passbook_type_id,
                                       balance_amount=balance_amount)

        transaction = dao.add_transaction_slip(passbook_id=passbook.id,
                                               customer_id=passbook.customer_id,
                                               employee_id=current_user.id,
                                               transaction_type=TransactionType.OPEN_PASSBOOK,
                                               transaction_amount=balance_amount,
                                               content="Tạo sổ tiết kiệm mới")

        return jsonify({"status": 200, "passbook": [passbook.dump()], "transaction_slip": [transaction.dump()]})
    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@app.route("/api/update-passbook", methods=["post"])
@decorator.login_required_user
def update_passbook():
    try:
        data = json.loads(request.data)
        passbook_id = data.get('passbook_id')
        passbook_type_id = data.get('passbook_type_id')
        balance_amount = data.get('balance_amount')

        passbook = dao.update_passbook(passbook_id=passbook_id,
                                       passbook_type_id=passbook_type_id,
                                       balance_amount=balance_amount)

        transaction = dao.add_transaction_slip(passbook_id=passbook.id,
                                               customer_id=passbook.customer_id,
                                               employee_id=current_user.id,
                                               transaction_type=TransactionType.OPEN_PASSBOOK,
                                               transaction_amount=balance_amount,
                                               content="Mở sổ tiết kiệm cũ")

        return jsonify({"status": 200, "passbook": [passbook.dump()], "transaction_slip": [transaction.dump()]})
    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@app.route("/api/update-passbook-deposit", methods=["post"])
@decorator.login_required_user
def update_passbook_deposit():
    try:
        data = json.loads(request.data)
        passbook_id = data.get('passbook_id')
        balance_amount = data.get('balance_amount')
        deposit_amount = data.get('deposit_amount')
        interest_amount = data.get('interest_amount')

        passbook = dao.update_passbook(passbook_id=passbook_id,
                                       balance_amount=int(balance_amount) + int(deposit_amount) + int(interest_amount))

        transaction = dao.add_transaction_slip(passbook_id=passbook.id,
                                               customer_id=passbook.customer_id,
                                               employee_id=current_user.id,
                                               transaction_type=TransactionType.DEPOSIT,
                                               transaction_amount=deposit_amount,
                                               interest_amount=interest_amount,
                                               content="Gửi tiền")

        return jsonify({"status": 200, "passbook": [passbook.dump()], "transaction_slip": [transaction.dump()]})
    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@app.route("/api/update-passbook-maturity", methods=["post"])
@decorator.login_required_user
def update_passbook_maturity():
    try:
        data = json.loads(request.data)
        passbook_id = data.get('passbook_id')

        passbook = dao.update_passbook(passbook_id=passbook_id)

        transaction = dao.add_transaction_slip(passbook_id=passbook.id,
                                               customer_id=passbook.customer_id,
                                               employee_id=current_user.id,
                                               transaction_type=TransactionType.MATURITY,
                                               transaction_amount=0,
                                               content="Đáo hạn")

        return jsonify({"status": 200, "passbook": [passbook.dump()], "transaction_slip": [transaction.dump()]})
    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@app.route("/api/update-passbook-withdraw", methods=["post"])
@decorator.login_required_user
def update_passbook_withdraw():
    try:
        data = json.loads(request.data)
        passbook_id = data.get('passbook_id')
        balance_amount = data.get('balance_amount')
        withdraw_amount = data.get('withdraw_amount')
        interest_amount = data.get('interest_amount')

        if int(balance_amount) == int(withdraw_amount):
            passbook = dao.update_passbook(passbook_id=passbook_id,
                                           balance_amount=int(balance_amount) - int(withdraw_amount))
        else:
            passbook = dao.update_passbook(passbook_id=passbook_id,
                                           balance_amount=int(balance_amount) - int(withdraw_amount) + int(interest_amount))

        transaction = dao.add_transaction_slip(passbook_id=passbook.id,
                                               customer_id=passbook.customer_id,
                                               employee_id=current_user.id,
                                               transaction_type=TransactionType.DEPOSIT,
                                               transaction_amount=withdraw_amount,
                                               interest_amount=interest_amount,
                                               content="Rút tiền")

        return jsonify({"status": 200, "passbook": [passbook.dump()], "transaction_slip": [transaction.dump()]})
    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@app.route("/api/create-customer", methods=["post"])
@decorator.login_required_user
def create_customer():
    try:
        data = json.loads(request.data)
        name = data.get('name')
        identity_card_number = data.get('identity_card_number')
        phone = data.get('phone')

        customer = dao.create_customer(name=name, identity_card_number=identity_card_number, phone=phone)
        return jsonify({"status": 200, "id": customer.id, "name": customer.name})
    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@app.route("/api/update-customer", methods=["post"])
@decorator.login_required_user
def update_customer():
    try:
        data = json.loads(request.data)
        customer_id = data.get('customer_id')
        phone = data.get('phone')

        customer = dao.update_customer(customer_id=customer_id, phone=phone)
        return jsonify({"status": 200, "customer": customer.dump()})
    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@app.route("/api/find-customer", methods=["post"])
@decorator.login_required_user
def find_customer():
    try:
        data = json.loads(request.data)
        customer_id = data.get('customer_id')
        identity_number = data.get('identity_number')
        name = data.get('name')

        customers = dao.find_customer(customer_id=customer_id, identity_number=identity_number, name=name)
        return jsonify({"status": 200, "customers": [c.dump() for c in customers]})

    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@app.route("/api/find-passbook-type", methods=["post"])
@decorator.login_required_user
def find_passbook_type():
    try:
        data = json.loads(request.data)
        passbook_type_id = data.get('passbook_type_id')

        passbook_types = dao.get_passbook_type(passbook_type_id=passbook_type_id)
        return jsonify({"status": 200, "passbook_types": [passbook_type.dump() for passbook_type in passbook_types]})

    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@app.route("/api/find-passbook", methods=["post"])
@decorator.login_required_user
def find_passbook():
    try:
        data = json.loads(request.data)
        passbook_id = data.get('passbook_id')
        customer_id = data.get('customer_id')
        passbook_type_id = data.get('passbook_type_id')
        open_date = data.get('open_date')

        passbooks = dao.get_passbook_list(passbook_id=passbook_id,
                                          customer_id=customer_id,
                                          passbook_type_id=passbook_type_id,
                                          open_date=open_date)
        return jsonify({"status": 200, "passbooks": [passbook.dump() for passbook in passbooks]})

    except Exception as ex:
        return jsonify({"status": 500, "error": ex})
