__all__ = ["taninv"]
from math import degrees, atan2

def taninv(dy, dx):
	return degrees(atan2(dy, dx))

if __name__ == "__main__":
	raise Exception("This is not a top level module")
