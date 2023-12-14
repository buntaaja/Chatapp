from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from wtform_fields import *
#from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'replace later'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fboecypywtrptr:0748b3a20a2fa3f0ef77dbbcb5c6d0a64022b55af2e6bc3bc52e912f5fa0383c@ec2-34-242-199-141.eu-west-1.compute.amazonaws.com:5432/d9vgh90ob3qi9f'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable Flask-SQLAlchemy event system
db = SQLAlchemy(app)

# This are the previous models.py
class User(db.Model):
    """ User model """

    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Check username exists
        user_object = User.query.filter_by(username=username).first()
        if user_object:
            return "Someone else has taken this username!"

        # Add user to DB
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted into DB!"


    return render_template("index.html", form=reg_form)

if __name__ == "__main__":
    app.run(debug=True)