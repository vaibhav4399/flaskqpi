from database.connection import me


class states(me.Document):

    meta = {"db_alias": "dbmisc"}

    _id = me.IntField(required=True, primary_key=True)
    name = me.StringField(required=True, unique=True)

    def get_id(self):
        return self._id
