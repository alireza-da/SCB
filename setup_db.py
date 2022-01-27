from replit import db
from user import User
import json

def add_users_to_db(list_users):
    users = db["users"]
    for user in list_users:
      print(user)
      _user = User(user.name, 0, 0, user.id)
      users.append(json.dumps(_user.__dict__))

def setup_tables(list_users):
    if "users" not in db.keys():
        db["users"] = []
        add_users_to_db(list_users)




def get_user(id):
  users = db["users"]
  for user in users:
    print(f"[INFO]: Retreiving user : {user}")
    _user = User.user_decoder(json.loads(user))
    print(f"[INFO]: Decode user to :{_user}")
    if _user.id == id:
      return _user
  return None


def get_user_id(id):
  users = db["users"]
  index = 0
  for user in users:
    
    _user = User.user_decoder(json.loads(user))
    
    if _user.id == id:
      return index
    index += 1
  return index

def get_user_occurance(id):
  users = db["users"]
  index = 0
  for user in users:
    _user = User.user_decoder(json.loads(user))
    if _user.id == id:
      index += 1
  return index

def set_user(user):
  d = json.dumps(user.__dict__)
  del db["users"][get_user_id(user.id)]
  print("[INFO]: Saving user: "+d)
  db["users"].append(d)  