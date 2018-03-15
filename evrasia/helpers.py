import os, re
from flask_restful import reqparse

def validNumber(phone_number):
    pattern = re.compile("^[\dA-Z]{3}[\dA-Z]{3}[\dA-Z]{3}[\dA-Z]{3}$", re.IGNORECASE)
    return True if phone_number.startswith('996') and pattern.match(phone_number) else False

def parse_arg_from_requests(arg, **kwargs):
	parse = reqparse.RequestParser()
	parse.add_argument(arg, **kwargs)
	args = parse.parse_args()
	return args[arg]