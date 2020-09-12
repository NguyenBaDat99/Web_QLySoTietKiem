function createCustomer() {
    if (identityNumber.value != "" && name.value != "") {
        fetch("/api/find-customer", {
            body: JSON.stringify({
                "identity_number": identityNumber.value,
                "name": name.value
            }),
            method: "post",
            headers: {"Content-Type": "application/json"}
        }).then(res => res.json()).then(data => {
            if (data.status == 200){
                msgCustomer.style = "";
                msgCustomer.innerText = "Khách hàng đã tồn tại"
            } else {
                fetch("/api/create-customer", {
                    body: JSON.stringify({
                        "name": name.value,
                        "identity_card_number": identityNumber.value,
                        "gender": gender.value,
                        "date_of_birth": dateOfBirth.value,
                        "phone": phone.value
                    }),
                    method: "post",
                    headers: {"Content-Type": "application/json"}
                }).then(res => res.json()).then(data => {
                    if (data.status == 200){
                        customerId.value = data.id;
                        customerName.value = data.name;
                        goPassbook();
                        msgCustomer.style = "display: none";
                    } else {
                        msgCustomer.style = "";
                        msgCustomer.innerText = data.error
                    }
                })
            }
        })
    } else {
        msgCustomer.style = "";
        msgCustomer.innerText = "Thiếu thông tin số CMND hoặc tên khách hàng"
    }
}


function createPassbook() {
    if (passbookType.value != "" && depositAmount.value != ""){
        fetch("/api/find-passbook-type", {
            body: JSON.stringify({
                "passbook_type_id": passbookType.value
            }),
            method: "post",
            headers: {"Content-Type": "application/json"}
        }).then(res => res.json()).then(data => {
            console.log(data)
            if (data.passbook_types[0].minimum_deposit <= depositAmount.value) {
                fetch("/api/create-passbook", {
                    body: JSON.stringify({
                        "customer_id": customerId.value,
                        "passbook_type_id": passbookType.value,
                        "open_date": openDate.value,
                        "balance_amount": depositAmount.value,
                    }),
                    method: "post",
                    headers: {"Content-Type": "application/json"}
                }).then(res => res.json()).then(data => {
                    goFinish();
                })
            } else {
                msgPassbook.style = "";
                msgPassbook.innerText = `Số tiền gửi phải lớn hơn ${data.passbook_types[0].minimum_deposit} VNĐ`;
            }
        })
    }else {
        msgPassbook.style = "";
        msgPassbook.innerText = "Vui lòng nhập đầy đủ thông tin"
    }
}


      function chooseCustomer(customer_id) {
        fetch("/api/find-customer", {
                body: JSON.stringify({
                    "customer_id": customer_id
                }),
                method: "post",
                headers: {"Content-Type": "application/json"}
            }).then(res => res.json()).then(data => {
                console.log(data);

                identityNumber.value = data.customers[0].identity_card_number;
                name.value = data.customers[0].name;
                phone.value = data.customers[0].phone;

                customerId.value = data.customers[0].id;
                customerName.value = data.customers[0].name;

                identityNumber.readOnly = true;
                name.readOnly = true;

                btnCreateAndContinue.style = "display: none";
                btnContinue.style = "";
                btnUpdateCustomer.style = "";
                btnBack.style = "";

                customerTableName.innerText = `Khách hàng: ${data.customers[0].name}`;
                fetch("/api/find-passbook", {
                  body: JSON.stringify({
                    "customer_id": data.customers[0].id
                  }),
                  method: "post",
                  headers: {"Content-Type": "application/json"}
                }).then(res => res.json()).then(data => {
                    customerTablePassbook.innerHTML = '';
                    data.passbooks.forEach(passbook => {
                        let date = new Date(passbook.open_date);
                        let amount = numberWithCommas(passbook.balance_amount);
                        let passbook_id_for_transaction = passbook.id;
                        let url_for_transaction =
                        "{{ url_for('transaction_passbook', passbook_id=" + passbook_id_for_transaction + ") }}";

                        if (passbook.balance_amount == 0){
                            customerTablePassbook.innerHTML +=
                            `<tr>
                            <th scope="row">${passbook.id}</th>
                            <td>${passbook.passbook_type_id}</td>
                            <td>${amount} VNĐ</td>
                            <td>${date.toLocaleDateString()}</td>
                            <td>
                                <button class="btn btn-primary" onClick="goPassbookOld(${passbook.id})">Mở sổ</button>
                            </td>
                            </tr>`;
                        } else {
                            customerTablePassbook.innerHTML +=
                            `<tr>
                            <th scope="row">${passbook.id}</th>
                            <td>${passbook.passbook_type_id}</td>
                            <td>${amount} VNĐ</td>
                            <td>${date.toLocaleDateString()}</td>
                            <td>
                                <a class="btn btn-warning"
                                href="${url_for_transaction}">
                                    Giao dịch
                                </a>
                            </td>
                            </tr>`;
                        }

                    })
                })
            })
      }


function updateCustomer() {
        fetch("/api/update-customer", {
            body: JSON.stringify({
                "customer_id": customerId.value,
                "phone": phone.value
            }),
            method: "post",
            headers: {"Content-Type": "application/json"}
        }).then(res => res.json()).then(data => {
            console.log(data);
            alert("Cập nhật thông tin khách hàng thành công");
        })
      }


      function updatePassbook() {
        if (passbookType.value != "" && depositAmount.value != ""){
            fetch("/api/find-passbook-type", {
                body: JSON.stringify({
                    "passbook_type_id": passbookType.value
                }),
                method: "post",
                headers: {"Content-Type": "application/json"}
            }).then(res => res.json()).then(data => {
                console.log(data)
                if (data.passbook_types[0].minimum_deposit <= depositAmount.value) {
                    fetch("/api/update-passbook", {
                        body: JSON.stringify({
                            "passbook_id": passbookId.value,
                            "passbook_type_id": passbookType.value,
                            "balance_amount": depositAmount.value
                        }),
                        method: "post",
                        headers: {"Content-Type": "application/json"}
                    }).then(res => res.json()).then(data => {
                        console.log(data)
                        goFinish();
                    })
                } else {
                    msgPassbook.style = "";
                    msgPassbook.innerText = `Số tiền gửi phải lớn hơn ${data.passbook_types[0].minimum_deposit} VNĐ`;
                }
            })
        }else {
            msgPassbook.style = "";
            msgPassbook.innerText = "Vui lòng nhập đầy đủ thông tin"
        }
      }

      function drawFormFinish(title, passbook_id, customer, time, amount) {
        formFinish.innerHTML =
        `<div class="container">
            <div class="row">
                <h1 class="display-4" style="font-size: 1.8rem;">${title}</h1>
            </div>
                <div class="dropdown-divider"></div>
            <form>
                <div class="form-group">
                    <label>Mã sổ: &{passbook_id}</label>
                </div>
                <div class="form-group">
                    <label>Khách hàng: &{customer}</label>
                </div>
                <div class="form-group">
                    <label>Thời gian giao dịch: &{time}</label>
                </div>
                <div class="form-group">
                    <label>Số tiền giao dịch: &{amount}</label>
                </div>
            </form>
        </div>`;
      }

      function updatePassbookDeposit() {
        if (depositAmount.value != ""){
            if ({{ passbook_type.minimum_deposit }} <= depositAmount.value) {
                fetch("/api/update-passbook", {
                    body: JSON.stringify({
                        "passbook_id": {{ passbook.id }},
                        "balance_amount": depositAmount.value
                    }),
                    method: "post",
                    headers: {"Content-Type": "application/json"}
                }).then(res => res.json()).then(data => {
                    console.log(data)
                    goFinish();
                })
            } else {
                msgDeposit.style = "";
                msgDeposit.innerText = "Số tiền gửi thêm phải lớn hơn" +
                {{ "{:,.0f}".format(passbook_type.minimum_deposit) }} + VNĐ;
            }
        }else {
            msgDeposit.style = "";
            msgDeposit.innerText = "Vui lòng nhập đầy đủ thông tin"
        }
      }