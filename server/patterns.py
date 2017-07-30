import time
import colorsys
from . import shared
from neopixel import * 
import math
import random

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

# ========================== #
#		   Utils 			 #
# ========================== #

def wheel(pos):
	# genereate wheel across STRIP_LENGTH
	pos = pos % 256
	if pos < 85:
		return RGBColor(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return RGBColor(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return RGBColor(0, pos * 3, 255 - pos * 3)

def rainbowSurjection(hue):
	return HSVColor(hue, 1, 1)

def rainbowSurjection2(hue):
	return HSVColor(hue**2, 1, 1)

def setAll(color):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)

def randomColor():
	hue = random.random()
	return HSVColor(hue, 1, 1)

def RGBColor(red, green, blue, white=0):
	brightness = shared.brightness.value/100.0
	red = max(min(int(round(red*brightness)), 255),0)
	green = max(min(int(round(green*brightness)), 255),0)
	blue = max(min(int(round(blue*brightness)), 255),0)
	white = max(min(int(round(white*brightness)), 255),0)
	return Color(green, red, blue, white)

# 0-1 for hue, 0-1 for saturation, 0-1 for value, 0-1 for white
def HSVColor(hue, saturation, value, white=0):
	red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
	return RGBColor(255*red, 255*green, 255*blue, white)





# ========================== #
#		   Patterns			 #
# ========================== #
def rainbow(strip=strip, wait_ms=100, num_colors=360):
	maxSpeed = 2
	minSpeed = 200
	
	for j in range(256):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel(int(j) & 255))
		strip.show()
		wait = (1-shared.speed.value/100.0)*minSpeed + maxSpeed
		time.sleep(wait/1000)

def rainbowFix(strip=strip):
	maxSpeed = 2
	minSpeed = 200
	
	for j in range(360):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, rainbowSurjection2((j/360.0)))
		strip.show()

		wait = (1-shared.speed.value/100.0)*minSpeed + maxSpeed
		time.sleep(wait/1000)

def rainbowCycle(wait_ms=20, iterations=5):
	maxSpeed = 20
	minSpeed = 200
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel(int((i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		wait = (1-shared.speed.value/100.0)*(minSpeed-maxSpeed) + maxSpeed
		time.sleep(wait/1000)

def rainbowStrobe(wait_ms=20, iterations=100):
	maxSpeed = 10
	minSpeed = 400

	for j in range(iterations):
		setAll(randomColor())
		strip.show()
		time.sleep(30/1000)
		setAll(RGBColor(0,0,0))
		strip.show()
		wait = (1-shared.speed.value/100.0)*(minSpeed-maxSpeed) + maxSpeed
		time.sleep(wait/1000)

def strobe(wait_ms=20, iterations=100):
	maxSpeed = 10
	minSpeed = 400

	for j in range(iterations):
		setAll(RGBColor(0,0,0,255))
		strip.show()
		time.sleep(30/1000)
		setAll(RGBColor(0,0,0))
		strip.show()
		wait = (1-shared.speed.value/100.0)*(minSpeed-maxSpeed) + maxSpeed
		time.sleep(wait/1000)

def wavetest(iterations=100000):
	i = 100
	# f = lambda x: math.cos((2*math.pi/40)*x)
	# for k in range(0, 11):
	# 	print(k, '-->', f(k))
	f = lambda x, test: 1 - (x/10)**test 
	while True:
		i = (i + 1) % 300
		setAll(RGBColor(0,0,0))
		for k in range(0, 11):
			testvar = shared.generic2.value/10.0 
			value = f(k, testvar)
			strip.setPixelColor(i+k, HSVColor(0.5, 1, value))
			strip.setPixelColor(i-k, HSVColor(0.5, 1, value))
		strip.show()

		wait = (1-shared.speed.value/100.0)*(390) + 10 
		time.sleep(wait/1000)

def colorWipe(wait_ms=50):
	this = theaterChase
	for i in range(strip.numPixels()):
		if statusCheck(this, controller):
			color = controller.color
			strip.setPixelColor(i, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
		else:
			return

def theaterChase(controller, wait_ms=50, iterations=10):
	this = theaterChase
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def theaterChaseRainbow(controller, wait_ms=50):
	this = theaterChaseRainbow
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				if statusCheck(this, controller):
					strip.setPixelColor(i, wheel(((i * 256 / strip.numPixels()) + j) & 255))
				else:
					return
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)