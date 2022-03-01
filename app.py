
from flask import Flask, render_template, redirect, url_for, flash, request, session, g, jsonify
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World! 2"