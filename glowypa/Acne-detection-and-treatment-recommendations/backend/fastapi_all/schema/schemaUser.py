from datetime import datetime

def userFormat(user) -> dict:
    return {
        "id": str(user['_id']),
        "first_name": user['first_name'],
        "last_name": user['last_name'],
        "birth_date": user['birth_date'],
        "skin_type": user['skin_type'],
        "location": user['location'],
        "email": user['email'],
        "password": user['password']
    }