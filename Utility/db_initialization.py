import pyrebase


def initialize_db():
    config = {
        'apiKey': "AIzaSyC1Cp2QUqKsh5BTSb-FpD_7ACpGIRFoy3c",
        'authDomain': "chatapp-639fe.firebaseapp.com",
        'databaseURL': "https://chatapp-639fe-default-rtdb.europe-west1.firebasedatabase.app",
        'projectId': "chatapp-639fe",
        'storageBucket': "chatapp-639fe.appspot.com",
        'messagingSenderId': "21711071743",
        'appId': "1:21711071743:web:96771ba09cfc69d25a9fca",
        'measurementId': "G-X69Q7TM1T8"
    }

    firebase = pyrebase.initialize_app(config)
    return firebase
