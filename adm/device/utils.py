from datetime import datetime
from datetime import timedelta

import jwt

def encode_password_as_jwt(device_id, auth_keyid, secret, exp_str=None):
    """
    :param auth_keyid: the id of the authentication key in the database
    :param secret: private symmetric  key
    :param exp_str: expiration time of the JWT. Example '09/19/18 13:55:26'. One Month if None
    :return: the jwt encoded string
    """
    # datetime_str = '09/19/18 13:55:26'
    # datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
    if not exp_str:
        exp = datetime.utcnow() + timedelta(days=31)
    else:
        exp = datetime.strptime(exp_str, '%m/%d/%y %H:%M:%S')
    encoded_jwt = jwt.encode({'sub': device_id, 'exp': exp, 'key': auth_keyid}, secret, algorithm='HS256')
    return encoded_jwt