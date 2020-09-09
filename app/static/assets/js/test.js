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
                        customerTablePassbook.innerHTML +=
                        `<tr>
                        <th scope="row">{{ passbook.id }}</th>
                        <td>{{ passbook.customer_id }}</td>
                        <td>{{ passbook.passbook_type_id }} - {{ passbook.passbook_type_id }}</td>
                        <td>{{ passbook.balance_amount }}</td>
                        <td>{{ passbook.open_date }}</td>
                        <td>
                            <button class="btn btn-warning">Giao dịch</button>
                        </td>
                        </tr>`;
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