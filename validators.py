import jsonschema
import hashlib
from aiohttp import web
import config

USER_POST = {
    'type': 'object',
    'properties':  {
        'name': {
            'type': 'string'
        },
        'password': {
            'type': 'string'
        },
        'email': {
            'type': 'string',
        }
    },
    'required': ['name', 'password', 'email']
}

ADV_POST = {
    'type': 'object',
    'properties':  {
        'title': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        },
        'owner_id': {
            'type': 'integer'
        }
    },
    'required': ['title', 'owner_id']
}


def validate_user_post(data):
    try:
        jsonschema.validate(data, schema=USER_POST)
        password = data['password']
        pass_hash = hashlib.md5(password.encode()).hexdigest() + config.SALT
        data['password'] = pass_hash
        return data
    except jsonschema.ValidationError:
        raise web.HTTPBadRequest(text='Ошибка ввода данных')


def validate_adv_post(data):
    try:
        jsonschema.validate(data, schema=ADV_POST)
        return data
    except jsonschema.ValidationError:
        raise web.HTTPBadRequest(text='Ошибка ввода данных')
