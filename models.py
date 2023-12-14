from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """ User model """

    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    # db.create_all()
    # you can also type into command line:
    # & "C:\Program Files\PostgreSQL\16\bin\psql" postgresql://fboecypywtrptr:0748b3a20a2fa3f0ef77dbbcb5c6d0a64022b55af2e6bc3bc52e912f5fa0383c@ec2-34-242-199-141.eu-west-1.compute.amazonaws.com:5432/d9vgh90ob3qi9f
    # And then do as in SQL (CREATE TABLE..)
    # d9vgh90ob3qi9f=> CREATE TABLE users(
    #   d9vgh90ob3qi9f(> id SERIAL PRIMARY KEY,
    #   d9vgh90ob3qi9f(> username VARCHAR(25) UNIQUE NOT NULL,
    #   d9vgh90ob3qi9f(> password TEXT NOT NULL
    #   d9vgh90ob3qi9f(> );
    #   CREATE TABLE
    #   d9vgh90ob3qi9f=> """