###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required # Here, too
from flask_sqlalchemy import SQLAlchemy
import omdb 

## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/kaylawiSI364midterm"

## All app.config values


## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################




##################
##### MODELS #####
##################

class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    director = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})". format(self.director,self.id)


class Title(db.Model):
    __tablename__ = "titles"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.title, self.id)


class Name(db.Model):
    __tablename__ = "names"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.name, self.id)



###################
###### FORMS ######
###################

class NameForm(FlaskForm):
    name = StringField("Please enter your name.",validators=[Required()])
    submit = SubmitField()

class DirectorTitleForm(FlaskForm):
    title_name = StringField("Enter the name of the movie: ", validators=[Required(),Length(min=1,max=280)])
    director_name = StringField("Enter the name of the director: ", validators=[Required(),Length(min=1,max=280)])
    submit = SubmitField('Submit')
#######################
###### VIEW FXNS ######
#######################

@app.route('/')
def home():
    form = NameForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
    if form.validate_on_submit():
        name = form.name.data
        newname = Name(name)
        db.session.add(newname)
        db.session.commit()
        return redirect(url_for('all_names'))
    return render_template('base.html',form=form)

@app.route('/names')
def all_names():
    names = Name.query.all()
    return render_template('name_example.html',names=names)

###################################
##### Routes & view functions #####
###################################

## Error handling routes - PROVIDED
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500




## Code to run the application...

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
