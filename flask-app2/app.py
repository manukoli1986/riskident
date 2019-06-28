#!/usr/bin/env python3
#Importing module of flask framework to run app on web
from flask import Flask, render_template
import datetime


# Create the application.
app = Flask(__name__)


# Displays the index page accessible at '/'
@app.route("/")
def index():
    return "This is second deployment. Kindly use /image uri to get output"

# Displays the image and text page accessible at '/image' and below is function.
@app.route("/image")
def image():
    print ("Hello World !!! - v2")
    return render_template('index.html')

# This code is finish and ready to server on port 80
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
