from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET-KEY']='oh-so-secret'
debug = DebugToolbarExtension(app)

