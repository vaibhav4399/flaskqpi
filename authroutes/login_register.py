from database.usermodel import users
from flask import make_response, jsonify, Blueprint, request
from flask_expects_json import expects_json
import json
from auth.auth_jwt import generate_token
import re

login_register = Blueprint("login_register", __name__)

error = {
    "error": True,
    "message": ""
}

email_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@login_register.route("/login/", methods=["GET", "POST"])
def login():

    body = request.data
    body = body.decode("utf-8")
    body = json.loads(body)
    if body.get("email") and body.get("password") and email_re.match(body.get("email")):
        user = users.objects(email=body.get("email")).first()
        if user:
            if user.verify_password(body.get("password")):
                user = json.loads(user.to_json())
                user.pop("password")
                user.pop("email")
                user.pop("id")
                user["error"] = False
                user["token"] = generate_token(user.get("id"))
                return make_response(user, 200)
            else:
                error["message"] = "Password does not match"
        else:
            error["message"] = "User does not exists"
    else:
        error["message"] = "Invalid credentials"
    return make_response(jsonify(error), 401)


@login_register.route("/register/", methods=["POST"])
def register():
    body = request.get_json()

    if body.get("name") and body.get("email") and body.get("password") and body.get("confirmpassword") and email_re.match(body.get("email")):
        user = users.objects(email=body.get("email")).first()
        if not user:
            if body.get("password") == body.get("confirmpassword") and len(body.get("password")) >= 8:
                user = users(name=body.get("name"),
                             email=body.get("email"),
                             password=body.get("password"))
                user.password = user.hash_pass(user.password)
                try:
                    user.save()
                    user = json.loads(user.to_json())
                    user.clear()
                    user["error"] = False
                    user["message"] = "OK"
                    return make_response(user, 200)
                except Exception as e:
                    error["message"] = "Something went wrong please try again later"
            else:
                error["message"] = "Password does not match or less than 8 characters"
        else:
            error["message"] = "User exists"
    else:
        error["message"] = "Invalid Credentials"
    return make_response(jsonify(error), 400)
