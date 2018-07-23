import time
from . import patterns
from .alarm import alarm
import os
import signal
from multiprocessing import Process
from . import shared
import subprocess

enabledPatterns = ["rainbow", "rainbowCycle"]
patternMap = {}

class PatternInfo:
	def __init__(self, patternId, patternFunction):
		self.patternId = patternId
		self.patternFunction = patternFunction
		self.pid = None
		self.status = None
		self.process = None

def addPattern(pattern): # Removing pattern authentication for now 
	if pattern in dir(patterns):
		if pattern not in patternMap.keys():
			patternFunc = getattr(patterns, pattern)
			patternMap[pattern] = PatternInfo(pattern, patternFunc)
		changePattern(pattern)
		return "Success"
	else:
		return "Pattern doesn't exist"

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
			#   os.kill(p, signal.SIGSTOP) 
			# except Exception as e:
			#   print 'Deleting thread weird stuff'
			#   return 'Error'
			# else:
			#   p.status = 'inactive'

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
		p.process = Process(target=patternloop, name=targetPattern, args=(p.patternFunction, p.patternId))
		p.status = 'pending'
		p.process.start()
		p.pid = p.process.pid
		p.status = 'active'
		print('Created process for pattern:', p.patternId, p.pid, p.status)

def suspendAll():
	for key in patternMap:
		p = patternMap[key]
		if p.pid != None:
			os.kill(p.pid, signal.SIGSTOP)
			p.status = "inactive"

def patternloop(patternFunc, patternId):
	print('pattern name:', patternId)
	print('module name:', __name__)
	print('parent process:', os.getppid())
	print('process id:', os.getpid())
	print('group id:', os.getpgrp())

	while True:
		patternFunc()


def setAttribute(value, attribute):
	getattr(shared, attribute).set(int(value))	

def setBrightness(brightness):
	if 0 <= brightness and brightness <= 100:
		shared.brightness.set(int(brightness))
		print(("Brightness set to: ", brightness))
	else:
		print("brightness out of bounds")

def setSpeed(speed):
	if 0 <= speed and speed <= 100:
		shared.speed.set(int(speed))
		print(("Speed set to: ", speed))
	else:
		print("speed out of bounds")
		

def alarm_fire():
	print("FIRING =======")
	alarm.cancelAlarm()
	suspendAll()
	patterns.setAll(patterns.RGBColor(0,0,0))
	patterns.strip.show()

	# Turn outlet ON
	subprocess.call('/var/www/rfoutlet/codesend 87347 -l 180 -p 0', shell=True)
	patterns.alarm()

