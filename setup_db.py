from user import User, Admin
import json

db = dict()

admins_id = [665530648789909504, 583223852641812499]


def add_users_to_db(list_users):
    users = db["users"]
    for user in list_users:
        print(f"user detail: {user.name, user.id}")
        _user = User(user.name, 0, 0, user.id)
        if not get_user(_user.id):
            users.append(json.dumps(_user.__dict__))


def add_admins(list_users):
    for user in list_users:
        if user.id in admins_id:
            _user = Admin(user.name, 0, 0, user.id)
            db["admins"].append(json.dumps(_user.__dict__))


def setup_tables(list_users):
    # print(f"[INFO]: user detail: {[user for user in list_users]}" )
    if "users" not in db.keys():
        db["users"] = []
        add_users_to_db(list_users)
        db["admins"] = []
        add_admins(list_users)


def delete_tables():
    del db["users"]
    del db["admins"]


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
    print("[INFO]: Saving user: " + d)
    db["users"].append(d)


def get_admin(user):
    for admin in db["admins"]:
        _user = user
        print(type(user))
        admin = User.user_decoder(json.loads(admin))
        if admin.id == _user.id:
            _user = Admin(_user.username, _user.social_credit, _user.level, _user.id)
            return _user
    return None


def delete_db():
    del db["users"]



def create_connection():
  pass