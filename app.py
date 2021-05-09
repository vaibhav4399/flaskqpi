from flask import Flask
from flask_cors import CORS
from authroutes.login_register import login_register
from authroutes.cropyield import crop_yield

app = Flask(__name__)
cors = CORS(app)


app.url_map.strict_slashes = False

app.register_blueprint(login_register, url_prefix="/api/auth")
app.register_blueprint(crop_yield, url_prefix="/api/user")


if __name__ == '__main__':
    app.run()
