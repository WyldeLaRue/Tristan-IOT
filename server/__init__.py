from flask import Flask

app = Flask(__name__, template_folder=".", static_url_path='/public')


class Object:
	def __init__(self):
		self.color = "orange"
		self.value = 1
		self.status = "active"

	def info(self):
		print("color: ", self.color)
		print("value: ", self.value)
		print("status: ", self.status) 

testObject = Object()

from .homepage import hello
