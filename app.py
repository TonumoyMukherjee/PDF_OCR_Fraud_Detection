# -*- coding: utf-8 -*-
"""
Created on Tue May 24 17:09:10 2022

@author: tonum
"""
from unicodedata import name
from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)

print(app)

@app.route("/new")
def home():
    print("123")
    return render_template("index.html",name="Ton")



if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)
    