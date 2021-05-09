import jwt
import os
import datetime
from functools import wraps
from flask import request, make_response, jsonify
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

error = {
    "error": True,
    "message": ""
}


def verify_token(func):
    @ wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            error["message"] = "Token not found"
            return make_response(jsonify(error), 400)

        try:
            payload = jwt.decode(token, os.getenv("JWT_SECRET"))
        except Exception as e:
            error["message"] = "Invalid token"
            return make_response(jsonify(error), 400)
        return func(payload,*args, **kwargs)
    return decorated


def generate_token(id):

    token = jwt.encode({"user": id}, os.getenv("JWT_SECRET"))

    return token.decode("utf-8")
