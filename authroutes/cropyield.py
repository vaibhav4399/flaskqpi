from flask import Blueprint, make_response, jsonify, request
import json
from pickle import load
from flask_expects_json import expects_json
import numpy as np
import os
from database.cropmodel import crops
from database.seasonmodel import seasons
from database.statemodel import states
from auth.auth_jwt import verify_token

crop_yield = Blueprint("crop_yield", __name__)

error = {
    "error": True,
    "message": "Invalid Details"
}


@crop_yield.route("/cropyield/", methods=["POST"])
@expects_json()
@verify_token
def cropyield(payload):

    body = request.get_json()
    if body["State"] and body["Season"] and body["Crop"] and body["Rainfall"] and body["Temperature"] and body["Area"]:

        state = states.objects(name=body["State"]).first()._id
        season = seasons.objects(name=body["Season"]).first()._id
        crop = crops.objects(name=body["Crop"]).first()._id
        rainfall = body["Rainfall"]
        temperature = body["Temperature"]
        area = body["Area"]

        x = [[state, season, crop, rainfall, temperature, area]]
        x = np.array(x)
        fi = open(os.getcwd() + "/models/model.pkl", "rb")
        model = load(fi)

        prediction = model.predict(x)
        if prediction:
            ans = {
                "error": False,
                "prediction": prediction[0],
            }
            return make_response(jsonify(ans), 200)
        else:
            error["message"] = "Something went wrong"

    return make_response(jsonify(error), 400)
