import mongoengine as me
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

me.connect(host=os.getenv("MONGO_URI"), db="User", alias="dbuser")
me.connect(host=os.getenv("MONGO_URI"), db="Misc", alias="dbmisc")
