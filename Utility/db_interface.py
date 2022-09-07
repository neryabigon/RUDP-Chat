import pyrebase
from Utility import db_initialization
from datetime import datetime


def add_user(auth, db, username, password, email):
    auth.create_user_with_email_and_password(email, password)
    auth_token = auth.sign_in_with_email_and_password(email, password)
    token_id = auth_token['idToken']
    new_user = {
        'username': username,
        'email': email,
        'online': True,
    }
    db.child('users').child(username).set(new_user, token_id)
    return token_id


def login_user(auth, db, username, password, email):
    auth_token = auth.sign_in_with_email_and_password(email, password)

    token_id = auth_token['idToken']
    user = {
        'online': True,
    }
    db.child('users').child(username).update(user, token_id)
    return token_id


def logout_user(db, username, token_id):
    user = {
        'online': False,
    }
    db.child('users').child(username).update(user, token_id)


def refresh_token(auth, token_id):
    auth.refresh(token_id)
    return auth.get_account_info(token_id)['users'][0]['idToken']


def is_verified(auth, token_id):
    user = auth.get_account_info(token_id)
    return user['users'][0]['emailVerified']


def get_user_id(auth, token_id):
    user = auth.get_account_info(token_id)
    return user['users'][0]['localId']


def verify_email(auth, token_id):
    auth.send_email_verification(token_id)


def get_online_users(db):
    users = db.child('users').get()
    online_users = []
    for user in users.each():
        if user.val()['online']:
            online_users.append(user.val()['username'])
    return online_users


def get_users(db):
    users = db.child('users').get()
    users_list = []
    for user in users.each():
        users_list.append(user.val()['username'])
    return users_list


#TODO
def push_message(db, username, message, send_to):
    if send_to == 'all':
        msg = {
            'sender': username,
            'receiver': 'all',
            'message': message,
            'timestamp': datetime.now()
        }
        db.child('messages').push(msg)
    else:
        msg = {
            'sender': username,
            'receiver': send_to,
            'message': message,
            'timestamp': datetime.now()
        }
        db.child('messages').push(msg)
