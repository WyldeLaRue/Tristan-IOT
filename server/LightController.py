import time
import patterns
import threading
from neopixel import *

# Strip Default Config 
LED_COUNT      = 300       # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 200    # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
LED_STRIP      = ws.SK6812_STRIP_RGBW	

class LightController:

	def __init__(self):
		self.loopStatus = True	# for debug only
		self.active = False
		self.strip = self.configureStrip()
		self.currentPattern = patterns.rainbow
		self.speed = 0.5

	def createThread(self):
		if not self.active:
			self.thread = threading.Thread(target=self.mainloop)
			self.thread.start()
			print "thread created"

	def mainloop(self):
		if not self.active:
			print "made it to loop function"
			self.active = True
			while self.loopStatus == True:
				self.currentPattern(self.strip, self)

	def configureStrip(brightness=100):
		strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
		strip.begin()
		return strip

	def debug(self):
		print "lc debug"



lc = LightController()
		
