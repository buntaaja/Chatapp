from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManeger, login_user, current_user, login_required, logout_user
from wtform_fields import*
from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'replace later'

# Configure database
app.config('SQLALCHEMY_DATABASe_URI') = 'postgres://
...'
db = SQLAlchemy(app)
