from user import User, Admin
from credentials import db_url
import json
import psycopg2
import logging
import typing
import functools

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger(__name__)

db = dict()

admins_id = [665530648789909504, 583223852641812499]


def add_users_to_db(list_users):
    users = db["users"]
    con, cursor = create_connection()

    insert_query = """INSERT INTO users(username, social_credits, id, level) """ \
                   """VALUES(%s, %s, %s, %s)"""
    values = []
    for user in list_users:
        # print(f"user detail: {user.name, user.id}")
        # try:
        #     cursor.execute(f"""INSERT INTO users(username, social_credits, id, level) """
        #                    f"""VALUES({user.name}, {0}, {user.id}, {user.id})""")
        # except Exception as e:
        #     print(e)
        _user = User(user.name, 0, 0, user.id)
        if (user.name, "0", str(user.id), "0") not in values:
            values.append((user.name, "0", str(user.id), "0"))
        if not get_user(_user.id):
            users.append(json.dumps(_user.__dict__))

    cursor.executemany(insert_query, values)
    con.commit()
    cursor.close()
    con.close()
    print_tables()


def add_admins(list_users):
    con, cursor = create_connection()
    insertion_sql = """INSERT INTO admins(username, social_credits, id, level) """ \
                    """VALUES(%s, %s, %s, %s)"""
    values = []
    for user in list_users:
        if user.id in admins_id:
            if (user.name, "0", str(user.id), "0") not in values:
                values.append((user.name, "0", str(user.id), "0"))
            _user = Admin(user.name, 0, 0, user.id)
            db["admins"].append(json.dumps(_user.__dict__))

    cursor.executemany(insertion_sql, values)
    con.commit()
    cursor.close()
    con.close()


def setup_tables(list_users):
    # print(f"[INFO]: user detail: {[user for user in list_users]}")
    con, cursor = create_connection()
    try:
        cursor.execute("""SELECT table_name FROM information_schema.tables
               """)
        tables = cursor.fetchall()
        if ("users",) not in tables:
            print("[INFO]: Creating Tables")
            cursor.execute(
                """CREATE TABLE users (
                    username VARCHAR(255),
                    social_credits INTEGER,
                    id BIGINT PRIMARY KEY,
                    level INTEGER
                )""")

        if ("admins",) not in tables:
            cursor.execute(
                """CREATE TABLE admins (
                    username VARCHAR(255),
                    social_credits INTEGER,
                    id BIGINT PRIMARY KEY,
                    level INTEGER
                )""")

        cursor.close()
        con.commit()
        con.close()
        add_users_to_db(list_users)
        add_admins(list_users)
    except Exception as e:
        print(f"[Error]: {e}")
    # print_tables()


def print_tables():
    print("[INFO]: Printing users Table")
    con, cursor = create_connection()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    print(result)
    cursor.close()
    con.commit()


def delete_tables():
    del db["users"]
    del db["admins"]


def get_user(id):
    user_ret = "SELECT * FROM users WHERE id = %s"
    con, cursor = create_connection()
    try:

        cursor.execute(user_ret, (id,))
        _user = cursor.fetchall()
        # print(f"[INFO]: Retrieving database user : {_user[0]}")
        user = User.user_decoder_static(_user[0])
        # print(f"[INFO]: Retrieving object user : {user}")
        con.commit()
        cursor.close()
        con.close()
        return user

    except Exception as e:
        print(f"[Error]: {e}")
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


def update_user(user):
    update_query = "UPDATE users SET username = %s, %s, %s, %s WHERE id = %s"
    con, cursor = create_connection()
    try:
        print(f"[INFO]: Saving user: {user.name}")
        cursor.execute(update_query, (user.name, user.social_credit, user.id, user.level, user.id))
        cursor.fetchall()
        con.commit()
        cursor.close()
        con.close()
    except Exception as e:
        print(e)


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
    try:
        con = psycopg2.connect(db_url)
        logger.info(f"[INFO]: Connected to DB {con}")
        return con, con.cursor()
    except Exception as e:
        logger.error(f"{e}")
