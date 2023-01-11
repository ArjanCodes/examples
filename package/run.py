# This run file is for testing purposes, supposing you have the package installed
from idgenerator.src.idgenerator import IdGenerator

print(IdGenerator(id_length=8).generate_numeric_id())
print(IdGenerator(id_length=10).generate_alphanumeric_id())
print(IdGenerator(id_length=12).generate_mixed_id())


