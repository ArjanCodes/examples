


ENCODE, DECODE = 0, 1

def EncodingManager(Func: callable, Op: int) -> str:
	assert Op in [0, 1], 'This Operation is not NotImplemented or incorrect!, index [%s]' % Op
	if Op == ENCODE:
		def Func_(s: str | bytes):
			assert isinstance(s, str) or isinstance(s, bytes), "This function can not encode %s Object" % str(type(s))
			if isinstance(s, str):
				s = s.encode()
			return Func(s).decode()
	elif Op == DECODE:
		def Func_(s: str | bytes):
			assert isinstance(s, str), "This function can not encode %s Object" % str(type(s))
			return Func(s).decode()
	return Func_
