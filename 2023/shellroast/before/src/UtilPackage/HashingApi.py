def Hasher(HashingFunc: callable, s: str | bytes) -> str:
    assert isinstance(s, str) or isinstance(s, bytes), (
        "This function can not hash a %s object" % str(type(s))
    )

    if isinstance(s, str):
        s = s.encode()

    return HashingFunc(s).hexdigest()
