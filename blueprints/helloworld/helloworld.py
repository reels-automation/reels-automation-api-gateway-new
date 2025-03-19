from flask import Blueprint, render_template, redirect

helloworld_bp = Blueprint("helloworld", __name__, template_folder="templates")

@helloworld_bp.route("/")
def index():
    return "Hello World!"

@helloworld_bp.route("/hello/<name>")
def hello_name(name):
    return f"Hello {name}"

#Broken = OP like a legendary scar