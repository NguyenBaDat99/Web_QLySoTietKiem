from app import app
import json
import os
import hashlib


# def load_admin():
#     with open(os.path.join(app.root_path, "data/admin_account.json"), encoding="utf-8") as f:
#         return json.load(f)
#
#
# def check_login(username, password):
#     admins = load_admin()
#
#     password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
#     for ad in admins:
#         if ad["username"].strip().lower() == username.strip().lower() and ad["password"] == password:
#             return ad
#
#     return None
