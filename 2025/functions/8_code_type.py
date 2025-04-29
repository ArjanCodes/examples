import types

# 3.10 Bytecode:
# 0 LOAD_FAST 0 (x)
# 2 LOAD_CONST 1 (42)
# 4 BINARY_ADD
# 6 RETURN_VALUE

bytecode = bytes(
    [
        124,
        0,  # LOAD_FAST x (arg 0)
        100,
        1,  # LOAD_CONST 42 (arg 1)
        23,
        0,  # BINARY_ADD
        83,
        0,  # RETURN_VALUE
    ]
)

constants = (None, 42)
varnames = ("x",)

# Create a CodeType for 3.10
code = types.CodeType(
    1,  # co_argcount
    0,  # co_posonlyargcount
    0,  # co_kwonlyargcount
    1,  # co_nlocals
    2,  # co_stacksize
    0x43,  # co_flags (OPTIMIZED | NEWLOCALS | NOFREE)
    bytecode,  # co_code
    constants,  # co_consts
    (),  # co_names
    varnames,  # co_varnames
    "<manual>",  # co_filename
    "add_42",  # co_name
    1,  # co_firstlineno
    b"\x00\x01",  # co_lnotab
    (),  # co_freevars
    (),  # co_cellvars
)

func = types.FunctionType(code, globals(), "add_42")

print(func(5))  # ✅ Output: 47
