import time
from . import patterns
import os
import signal
from multiprocessing import Process
from neopixel import *
from .patterns import rgbColor, hsvColor
from . import shared

# Strip Default Config 
LED_COUNT      = 300       # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255    # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
LED_STRIP      = ws.SK6812_STRIP_RGBW	



strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()
enabledPatterns = ["rainbow", "rainbowCycle"]
patternMap = {}

class PatternInfo:
	def __init__(self, patternId, patternFunction):
		self.patternId = patternId
		self.patternFunction = patternFunction
		self.pid = None
		self.status = None
		self.process = None

def addPattern(pattern):
    if pattern in enabledPatterns:
        if pattern not in patternMap.keys():
        	patternFunc = getattr(patterns, pattern)
        	patternMap[pattern] = PatternInfo(pattern, patternFunc)

		changePattern(patternFunc)
		return "Success"
		
   	else:
   		return "Pattern not enabled."

def changePattern(targetPattern):
	if targetPattern not in list(patternMap.keys()):
		return False

	if patternMap[targetPattern].status == "active":
		return True

	for key in patternMap:
		p = patternMap[key]
		if p.pid != None:
			os.kill(p.pid, signal.SIGSTOP)
			p.status = "inactive"
			# try:
			# 	os.kill(p, signal.SIGSTOP) 
			# except Exception as e:
			# 	print 'Deleting thread weird stuff'
			# 	return 'Error'
			# else:
			# 	p.status = 'inactive'

	p = patternMap[targetPattern]
	if p.pid != None and p.process != None:
		try:
			os.kill(p.pid, signal.SIGCONT)
		except Exception as e:
			print('issues with thread deletion')
			return 'Error' 
		else:
			p.status = True
	elif p.pid == None and p.process == None:
		print('Creating process for pattern:', p.patternId, p.pid, p.status)
		p.process = Process(target=patternloop, name=targetPattern, args=(p.patternFunction, strip))
		p.status = 'pending'
		p.process.start()
		p.pid = p.process.pid
		p.status = 'active'
		print('Created process for pattern:', p.patternId, p.pid, p.status)

def patternloop(patternFunc, strip):
	print('module name:', __name__)
	print('parent process:', os.getppid())
	print('process id:', os.getpid())
	print('group id:', os.getpgrp())

	while True:
		patternFunc(strip)

def setBrightness(self, brightness):
	if 0 <= brightness and brightness <= 100:
		shared.brightness.set(int(brightness))
		print(("Brightness set to: ", brightness))
	else:
		print("brightness out of bounds")

def setSpeed(self, speed):
	if 0 <= speed and speed <= 100:
		shared.speed.set(int(speed))
		print(("Speed set to: ", speed))
	else:
		print("speed out of bounds")
		
