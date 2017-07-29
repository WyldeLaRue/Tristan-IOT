import time
import colorsys
import shared
from neopixel import * 

stripBrightness = 0.5

# ========================== #
#		   Utils 			 #
# ========================== #
def statusCheck(function, controller): # asks controller if function should continue
	return (not (function == controller.currentPattern))

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return rgbColor(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return rgbColor(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return rgbColor(0, pos * 3, 255 - pos * 3)

def rgbColor(red, green, blue, white=0):
	brightness = shared.brightness.value/100.0
	return Color(int(green*brightness), int(red*brightness), int(blue*brightness), int(white*brightness))

# 0-1 for hue, 0-1 for saturation, 0-1 for brightness, 0-1 for white
def hsvColor(hue, saturation, brightness, white=0):
	red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
	return rgbColor(255*red, 255*green, 255*blue, white)





# ========================== #
#		   Patterns			 #
# ========================== #
def rainbow(strip, wait_ms=100, iterations=1):
	maxSpeed = 5
	minSpeed = 200
	
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((j) & 255))
		strip.show()

		wait = (1-shared.speed.value/100.0)*minSpeed + maxSpeed
		time.sleep(wait/1000)


def rainbowCycle(strip, wait_ms=20, iterations=5):
	maxSpeed = 20
	minSpeed = 200
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel(((i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		wait = (1-shared.speed.value/100.0)*(minSpeed-maxSpeed) + maxSpeed
		time.sleep(wait/1000)


def colorWipe(strip, wait_ms=50):
	this = theaterChase
	for i in range(strip.numPixels()):
		if statusCheck(this, controller):
			color = controller.color
			strip.setPixelColor(i, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
		else:
			return

def theaterChase(strip, controller, wait_ms=50, iterations=10):
	this = theaterChase
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				if statusCheck(this, controller):
					color = controller.color
					strip.setPixelColor(i+q, color)
				else:
					return
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def theaterChaseRainbow(strip, controller, wait_ms=50):
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