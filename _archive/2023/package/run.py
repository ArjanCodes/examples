from idgenerator import (
    generate_password,
    generate_guid,
    generate_credit_card_number,
    generate_object_id,
    generate_pin_number,
)

print(generate_password(length=8))

print(generate_guid())

print(generate_credit_card_number(length=16))

print(str(generate_pin_number(length=4)))

print(generate_object_id())
