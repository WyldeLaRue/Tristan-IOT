from . import shared
from . import LightController as lights


def debugMain():
	# print 'patternMap:', lights.patternMap
	print('brightness:', shared.brightness.value)
	print('speed:', shared.speed.value)



def printScope():
	print('dir():', dir())
	print('locals():', locals())
	print('====' * 10) 
	print('globals():')
	print('')
	for key in globals():
		print(key, globals()[key])