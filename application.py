from time import localtime, strftime
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
#from models import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256 #sha215 also exists
#from wtform_fields import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

# Configure app
app = Flask(__name__)
app.secret_key = 'replace later'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable Flask-SQLAlchemy event system
db = SQLAlchemy(app)

# Initialize Flask-SocketIO
socketio = SocketIO(app)
# define list of rooms
ROOMS = ["lounge", "news", "games", "coding"]

# Configure flask login
login = LoginManager(app)
login.init_app(app)

# This are the previous models.py
class User(UserMixin, db.Model): # Usermixin tells about user (it automatically adds a lot of methods to the class)
    """ User model """

    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

# This are the previous wtform_fields.py
def invalid_credentials(form, field):
    """ Username and password checker """
    username_entered = form.username.data
    password_entered = field.data

    # Check credentials are valid
    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Username or password is incorrect.")
    #elif password_entered != user_object.password:
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Username or password is incorrect")

class RegistrationForm(FlaskForm):
    """ Registration form """

    username = StringField('username_label', 
        validators=[InputRequired(message="Username required"),
        Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    password = PasswordField('password_label',
        validators=[InputRequired(message="Password required"),
        Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
    confirm_pswd = PasswordField('confirm_pswd_label',
        validators=[InputRequired(message="Password required"),
        EqualTo('password', message="Passwords must match")])
    submit_button = SubmitField('Create')
    
    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists. Select different username.")

class LoginForm(FlaskForm):
    """ Login form """

    username = StringField('username_label', 
        validators=[InputRequired(message="Username required")])
    password = PasswordField('password_label',
        validators=[InputRequired(message="Password required"),
        invalid_credentials])
    submit_button = SubmitField('Login')


@login.user_loader
def load_user(id):

    # User.query.filter_by(id=id).first()
    return User.query.get(int(id))

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()

    # Update DB is validation was successfull
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Check username exists
        # user_object = User.query.filter_by(username=username).first()
        # if user_object:
        #     return "Someone else has taken this username!"

        # Hash password
        hashed_pswd = pbkdf2_sha256.hash(password) #29.000 iterations

        # Add user to DB
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Registered succesfully. Please login.', 'success')
        
        return redirect(url_for('login'))


    return render_template("index.html", form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        # current_user.username gives us the username of current user
        # Let's check if current user is logged in with mixin
        # if current_user.is_authenticated:
            # return "Logged in with flask-login!"
        return redirect(url_for('chat'))
        
        #return "Not logged in :()"

    return render_template("login.html", form=login_form)

@app.route("/chat", methods=['GET', 'POST'])
#@login_required
def chat():
    # if not current_user.is_authenticated:
    #     flash('Please login.', 'danger') # name dange matches the bootstrap class
    #     return redirect(url_for('login'))

    return render_template('chat.html', username=current_user.username,
        rooms=ROOMS)

@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))


# Add event buckets for SocketIO
@socketio.on('message')
def message(data):

    print(f"\n\n{data}\n\n")
    # send(data) # By default it sends the data to event bucket called message
    # emit('some-event', 'this is a custom event message') # sends to the client event bucket called some-event
    # This is the username: current_user.username
    # pass out the username with template
    
    send({'msg': data['msg'], 'username': data['username'], 
        'time_stamp': strftime('%b-%d %I:%M%p', localtime())}, 
        room=data['room'])

@socketio.on('join')
def join(data):

    join_room(data['room'])
    send({'msg': data['username'] + " has joined the " + data['room'] + "room."}, 
        room=data['room'])

@socketio.on('leave')
def leave(data):

    leave_room(data['room'])
    send({'msg': data['username'] + " has left the " + data['room'] + "room."}, 
        room=data['room'])


if __name__ == "__main__":
    #app.run(debug=True)
    # flask socketio has its own
    socketio.run(app, debug=True)
