from . import shared
from . import lights as lights


def debugMain():
	# print 'patternMap:', lights.patternMap
	print('brightness:', shared.brightness.value)
	print('speed:', shared.speed.value)
	print('generic1:', shared.generic1.value)
	print('generic2:', shared.generic2.value)
	print('generic3:', shared.generic3.value)



def printScope():
	print('dir():', dir())
	print('locals():', locals())
	print('====' * 10) 
	print('globals():')
	print('')
	for key in globals():
		print(key, globals()[key])