from Utility import db_initialization

firebase = db_initialization.firebase
auth = db_initialization.auth
db = db_initialization.db

email = "nerya0002@gmail.com"
password = "12345678"

auth_token = auth.sign_in_with_email_and_password(email, password)
token_id = auth_token['idToken']

new_user = {
    'username': 'bob',
    'email': 'nerya0002@gmail.com',
    'online': True,
}
db.child('users').child('bob').set(new_user, token_id)