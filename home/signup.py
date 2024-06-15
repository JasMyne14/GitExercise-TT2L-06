from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from home import db
from .models import User
from .forms import SignUpForm

signup = Blueprint('signup', __name__)
