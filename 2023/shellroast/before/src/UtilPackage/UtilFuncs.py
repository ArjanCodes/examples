from json import loads
from dataclasses import dataclass


@dataclass
class Config:
    ALGORITHMS: set


def LoadConfig(configFilePath: str = "./Config.json") -> Config:
    """LOAD THE CONFIG File and sets the properties."""
    with open(configFilePath) as fp:
        Data = loads(fp.read())
        return Config(**Data)


def TestFunction():
    pass


# Success = 0
# ENCODE, DECODE = 0, 1
# DidNotWorkObj = {}
# # Test.
# for i in ALGO.keys():
# 	try:
# 		Encoded = ALGO[i][ENCODE]("String_")
# 	except Exception as e:
# 		print("ERROR: ", e)
# 		DidNotWorkObj[i] = [ENCODE]
# 	try:
# 		Decoded = ALGO[i][DECODE](Encoded)
# 	except Exception as e:
# 		print("ERROR: ", e)
# 		if i in DidNotWorkObj.keys():
# 			DidNotWorkObj[i].append(DECODE)
# 		else:
# 			DidNotWorkObj[i] = [DECODE]

# if DidNotWorkObj:
# 	print(DidNotWorkObj)
# else:
# 	print('sucess :)')
