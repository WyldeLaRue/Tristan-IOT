import time
from neopixel import * 


# ========================== #
#		   Utils 			 #
# ========================== #
def statusCheck(function, controller): # asks controller if function should continue
	return (not (function == controller.currentPattern))

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)



# ========================== #
#		   Patterns			 #
# ========================== #
def rainbow(strip, controller, wait_ms=100, iterations=1):
	this = rainbow
	slope = 1000 # in ms 
	intercept = 20 # in ms
	
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			if statusCheck(this, controller):
				return
			strip.setPixelColor(i, wheel((j) & 255))
		strip.show()
		speed = ((1 - controller.speed)*slope + intecept)/1000
		time.sleep(speed)


def rainbowCycle(strip, controller, wait_ms=20, iterations=5):
	this = rainbowCycle
	slope = 1000 # in ms 
	intercept = 20 # in ms
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			if statusCheck(this, controller):
				return
			strip.setPixelColor(i, wheel(((i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		speed = ((1 - controller.speed)*slope + intecept)/1000
		time.sleep(speed)


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