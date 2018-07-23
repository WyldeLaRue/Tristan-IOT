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

def	nuWheel(n):
	n = int(round(n))
	cycle = (n // 256) % 6
	n = n % 256
	if cycle == 0:
		red, green, blue = (255, 255-n, 0)
	elif cycle == 1:
		red, green, blue = (255, 0, n)
	elif cycle == 2:
		red, green, blue = (255-n, 0, 255)
	elif cycle == 3:
		red, green, blue = (0, n, 255)
	elif cycle == 4:
		red, green, blue = (0, 255, 255-n)
	elif cycle == 5:
		if 1.1 * n < 255:
			red, green, blue = (int(1.1*n), 255, 0)
		else:
			red, green, blue = (255, 255, 0)

	return RGBColor(red, green, blue)




def rainbowSurjection(hue):
	return HSVColor(hue, 1, 1)

def rainbowSurjection2(hue):
	return HSVColor(hue**2, 1, 1)

def setAll(color):
	for i in range(300):
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
	# print((hue, saturation, value), '-->', (255*red, 255*green, 255*blue))
	return RGBColor(255*red, 255*green, 255*blue, white)






# ========================== #
#		   Patterns			 #
# ========================== #
def rainbow(x=1, y=2):
	maxSpeed = 2
	minSpeed = 200
	
	for j in range(256*6):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, nuWheel(j))
		strip.show()
		wait = (1-shared.tickrate.value/100.0)*minSpeed + maxSpeed
		time.sleep(wait/1000)


def rainbowFix(strip=strip):
	maxSpeed = 2
	minSpeed = 200
	
	for j in range(360):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, rainbowSurjection2((j/360.0)))
		strip.show()

		wait = (1-shared.tickrate.value/100.0)*minSpeed + maxSpeed
		time.sleep(wait/1000)

def rainbowCycle(wait_ms=20, iterations=5):
	maxSpeed = 20
	minSpeed = 200
	for j in range(300):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, nuWheel(5.12*(i+j)))
		strip.show()
		wait = (1-shared.tickrate.value/100.0)*(minSpeed-maxSpeed) + maxSpeed
		time.sleep(wait/1000)


def rainbowReversed():
	while True:
		period = 500
		for t in range(-period, period):
			for pixel in range(strip.numPixels()):
				strip.setPixelColor(pixel, nuWheel((0.07*pixel*t)))
			strip.show()
			wait = (1-shared.tickrate.value/100.0)*(250) + 5
			time.sleep(wait/1000)
		for t in range(period, -period, -1):
			for pixel in range(strip.numPixels()):
				strip.setPixelColor(pixel, nuWheel((0.07*pixel*t)))
			strip.show()
			wait = (1-shared.tickrate.value/100.0)*(250) + 5
			time.sleep(wait/1000)

def rainbowExpansion():
	t = 0
	while True:
		for pixel in range(strip.numPixels()):
			strip.setPixelColor(pixel, nuWheel(5.12*(pixel*t)))
		strip.show()
		t += shared.ticksize.value
		wait = (1-shared.tickrate.value/100.0)*(390) + 10
		time.sleep(wait/1000)

def rainbowStrobe():
	maxSpeed = 10
	minSpeed = 600

	for j in range(10000):
		setAll(randomColor())
		strip.show()
		time.sleep(100/1000)
		setAll(RGBColor(0,0,0))
		strip.show()
		wait = (1-shared.tickrate.value/100.0)*(minSpeed-maxSpeed) + maxSpeed
		time.sleep(wait/1000)

def strobe(wait_ms=20):
	maxSpeed = 10
	minSpeed = 600

	for j in range(10000):
		setAll(RGBColor(0,0,0,255))
		strip.show()
		time.sleep(30/1000)
		setAll(RGBColor(0,0,0))
		strip.show()
		wait = (1-shared.tickrate.value/100.0)*(minSpeed-maxSpeed) + maxSpeed
		time.sleep(wait/1000)

def static():
	for j in range(1000):
		setAll(RGBColor(0,0,0,255))
		strip.show()
		time.sleep(0.5)


def alarm():
	DURATION = 10
	duration_seconds = DURATION * 60
	wait = duration_seconds/255.0
	for brightness in range(255):
		setAll(RGBColor(0, 0, 0, brightness + 1))
		strip.show()
		time.sleep(wait)

################################################################################################################################
#		EXPERIMENTAL PATTERNS
################################################################################################################################
def wavetest(iterations=100000):
	i = 100
	#f = lambda x, test: math.cos((2*math.pi/40)*x)
	#f = lambda x, test: 1 - (x/20)**test 
	f = lambda x, test: (1.0 / (1 + (0.35*x)**2))
	black = RGBColor(0,0,0)
	while True:
		i = (i + 1) % 300
		strip.setPixelColor(i-1, black)
		for j in range(10):
			dec = j/10.0
			for k in range(0, 23):
				testvar = shared.generic2.value/100.0 
				value = f(k+j, testvar)
			strip.setPixelColor(int(i+k+j), HSVColor(0, 1, value))
				#strip.setPixelColor(i-k, HSVColor(0.5, 1, value))
			strip.show()

		wait = (1-shared.tickrate.value/100.0)*(390) + 10 
		time.sleep(wait/1000)


def sintest(iterations=100000):
	def f(x, t):
		arg = 2*math.pi * (x - t/30.0) / 30.0 
		return 0.5 * math.sin(arg) + 0.5
	t = 0
	color1 = (255, 0, 0)
	color2 = (0, 0, 255)
	while True:
		t += 10
		for x in range(300):
			ratio = f(x, t)
			red, blue, green = colorMix(color1, color2, ratio)
			color = RGBColor(red, blue, green)
			strip.setPixelColor(x, color)
		strip.show()
		wait = (1-shared.tickrate.value/100.0)*(390) + 10 
		time.sleep(wait/1000)

def warmSinTest(iterations=100000):
	def f(x, t):
		arg = 2*math.pi * (x - t/30.0) / 30.0 
		return 0.5 * math.sin(arg) + 0.5
	t = 0
	while True:
		t += 10
		for x in range(300):
			ratio = f(x, t)
			color = RGBColor(0, 0, 0, ratio*255)
			strip.setPixelColor(x, color)
		strip.show()
		wait = (1-shared.tickrate.value/100.0)*(390) + 10 
		time.sleep(wait/1000)


def brightnessTest():
	print('===================')
	for i in range(300):
		strip.setPixelColor(i, RGBColor(0,0,0))
	for i in range(256):
		strip.setPixelColor(i+30, RGBColor(0, 0, i, debug=True))
	strip.show()
	wait = (1-shared.tickrate.value/100.0)*(390) + 10
	print('####################')
	time.sleep(10)


# ==============
def colorMix(color1, color2, ratio):
	inverse = 1-ratio
	red1, green1, blue1 = color1
	red2, green2, blue2 = color2

	red = red1*inverse + red2*ratio
	green = green1*inverse + green2*ratio
	blue = blue1*inverse + blue2*ratio
	return (red, green, blue)

def paletteMap(ratio, color1, color2, color3, color4):
	colors = (color1, color2, color3, color4)
	box = ratio * 3
	pos = box - math.floor(box)
	floorBox = math.floor(box)
	return colorMix(colors[floorBox],colors[(floorBox+1) % 4],pos)
	#box ranges from 0- 3
	#1, 2/3, 1/3, 0
	if ratio < 0.33:
		return colorMix(color2, color1)
	elif ratio < 0.66:
		return colorMix(color3, color2)
	else:
		return colorMix(color4, color3)

def crawlHelper(x,t):

	#sarina pallete
	# purple (205, 0, 242)
	# orange (255, 100, 0)
	main1 = (0, 0, 255)
	secondary1 = (0, 180, 180)
	secondary2 = (220, 150, 0)
	main2 = (255, 0, 0)
	length = 300
	frames = 30
	mul = 1
	offset = math.sin(2*math.pi*x/length*2)
	index = (t/frames) + (x/length) + offset
	inverse = 0.5*math.cos(math.pi + ((index*2*math.pi)*mul))+0.5
	return paletteMap(1-inverse, main1, secondary1, secondary2, main2)


def crawl():
	t = 0
	while True:
		for pixel in range(strip.numPixels()):
			red, blue, green = crawlHelper(pixel,t)
			strip.setPixelColor(pixel, RGBColor(red, blue, green))
		strip.show()
		t += shared.ticksize.value
		wait = (1-shared.tickrate.value/100.0)*(390) + 10
		time.sleep(wait/1000)

# ===========
################################################################################
		# OLD PATTERNS
################################################################################
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
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def theaterChaseRainbow(wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i, wheel(int((i * 256 / strip.numPixels()) + j) & 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)