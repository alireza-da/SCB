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
    # users = db["users"]
    con, cursor = create_connection()

    insert_query = """INSERT INTO users(username, social_credits, id, level) """ \
                   """VALUES(%s, %s, %s, %s)"""
    values = []
    users = get_all_user()
    uids = []
    for user in users:
        uids.append(user[2])

    for user in list_users:
        _user = User(user.name, 0, 0, user.id)
        value = (user.name, "0", str(user.id), "0")
        if value not in values and user.id not in uids:
            values.append((user.name, "0", str(user.id), "0"))
        # if not get_user(_user.id):
        #     users.append(json.dumps(_user.__dict__))

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
    admins = get_all_admins()
    print(admins)
    for user in list_users:
        if user.id in admins_id:
            value = (user.name, "0", str(user.id), "0")
            if value not in values and (user.name, 0, user.id, 0) not in admins:
                values.append(value)

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
    except Exception as e:
        print(f"[Error][Setup Tables]: {e}")
    add_users_to_db(list_users)
    add_admins(list_users)
    # print_tables()


def print_tables():
    print("[INFO]: Printing users Table")
    con, cursor = create_connection()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    print(result)
    cursor.close()
    con.commit()


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


def get_all_user():
    sql = "SELECT * FROM users"
    con, cursor = create_connection()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        con.commit()
        cursor.close()
        con.close()
        return result
    except Exception as e:
        print(f"[Error]: {e}")


def get_all_admins():
    sql = "SELECT * FROM admins"
    con, cursor = create_connection()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        con.commit()
        cursor.close()
        con.close()
        return result
    except Exception as e:
        print(f"[Error]: {e}")


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
    update_query = "UPDATE users SET username = %s, social_credits = %s, id = %s, level = %s WHERE id = %s"
    con, cursor = create_connection()
    try:
        print(f"[INFO]: Saving user: {user.username}")
        cursor.execute(update_query, (user.username, user.social_credit, user.id, user.level, user.id))
        con.commit()
        cursor.close()
        con.close()
    except Exception as e:
        print(f"[Error][setup_db.py]: {e}")


def get_admin(user):
    admin_ret = "SELECT * FROM admins WHERE id = %s"
    con, cursor = create_connection()
    try:
        cursor.execute(admin_ret, (user.id,))
        _user = cursor.fetchall()
        print(f"[INFO]: Retrieving database admin : {_user[0]}")
        admin = Admin.user_decoder_static(_user[0])
        print(f"[INFO]: Retrieving object admin : {admin}")
        con.commit()
        cursor.close()
        con.close()
        return admin
    except Exception as e:
        print(f"[Error]: {e}")
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
