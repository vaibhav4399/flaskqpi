from database.connection import me
import mongoengine_goodjson as gj
import bcrypt as b


class users(gj.Document):

    meta = {"db_alias": "dbuser"}

    name = me.StringField(required=True, nullable=False)
    email = me.StringField(required=True, nullable=False, unique=True)
    password = me.DynamicField(required=True, nullable=False)

    def get_id(self):
        return self.id

    def get_email(self):
        return self.email

    def verify_password(self, passw):
        # print(type(self.password, "Sdsdgrgrgrd"))
        if b.checkpw(passw.encode("utf-8"), self.password):
            return True
        return False

    def hash_pass(self, password):
        return b.hashpw(password.encode("utf-8"), b.gensalt())
