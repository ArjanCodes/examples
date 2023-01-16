# This run file is for testing purposes, supposing you have the package installed
# from idgenerator.src.idgenerator import *
import string

from package.app.idgenerator.src.idgenerator import generate_password, generate_guid, generate_credit_card_number, generate_object_id, generate_pin_number

print(generate_password(length=8))

guid = generate_guid()
print(guid)
parts = guid.split('-')
test = [char in string.hexdigits for part in parts for char in part]
print(all(test))

print(generate_credit_card_number(length=16))

print (str(generate_pin_number(length=4)))

print(generate_object_id())




