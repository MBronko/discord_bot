from dotenv import load_dotenv
from os import environ

load_dotenv()

DESCRIPTION = 'Discord Bot Under Development'

OWNER_ID = 322414584256266240

if environ['DEBUG'] not in ['True', 'False']:
    raise ValueError('invalid DEBUG value in .env file. Only True or False are accepted')

DEBUG = environ['DEBUG'] == 'True'

PREFIX_BLACKLIST = ['']

DEFAULT_PREFIX = '' if DEBUG else '!'
