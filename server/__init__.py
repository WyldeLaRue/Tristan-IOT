from flask import Flask

app = Flask(__name__, template_folder=".")
from homepage import hello
