###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,ValidationError # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required, Length # Here, too
from flask_sqlalchemy import SQLAlchemy
import omdb 
import json
import requests 

## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/kaylawiSI364midterm"

## All app.config values

app.config['SECRET_KEY'] = 'hard to guess string from si364'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


## Statements for db setup (and manager setup if using Manager)

db = SQLAlchemy(app) # For database use 


######################################
######## HELPER FXNS (If any) ########
######################################


def get_or_create_titles(db_session,title_name):
    title = db.session.query(Title).filter_by(title=title_name).first()
    if title:
        flash('title exists')
        return redirect(url_for('see_all_title'))
        #return title
    else:
        title = Title(title=title_name)
        db_session.add(title)
        db_session.commit
        return redirect(url_for('index'))
        #return title

def get_or_create_id(db_session, id_name):
    id = db.session.query(Id).filter_by(id = id_name).first()
    if id:
        flash("id exists")
        return redirect(url_for('see_all_id'))
        #return id
    else:
        id = Id(id = id_name)
        db_session.add(id)
        db_session.commit
        flash('id added successfully')
        return redirect(url_for('index'))
        #return id

##################
##### MODELS #####
##################


class Title(db.Model):
    __tablename__ = "titles"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64))
    directors = db.relationship('ids', backref = 'Title') # This shows relationship between directors and titles 

    def __repr__(self):
        return "{0} (ID: {1})".format(self.id, self.title, self.directors)

class Id(db.Model):
    __tablename__ = "ids"
    id = db.Column(db.Integer, primary_key=True)
  
    def __repr__(self):
        return "{0} (ID: {1})". format(self.id)

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
    name = StringField("Please enter your name:" ,validators=[Required(),Length(min=1,max=280)])
    submit = SubmitField('Submit')

    def validate_name(self,field):

        if field.data[0] == "@":
            raise ValidationError("Not a valid name")
       
        if len(field.data.split()) < 1: 
            raise ValidationError("Not a valid name")

class TitleIdForm(FlaskForm):
    title_name = StringField("Enter the name of the movie: ", validators=[Required(),Length(min=1,max=280)])
    id_number = IntegerField("Enter the id of the movie: ", validators=[Required(),Length(min=1,max=280)])
    submit = SubmitField('Submit')


    ## Custom Validation 

    def validate_title_name(self,field):

        if field.data[0] == "@" :
            raise ValidationError("Not a valid title")

        if field.data[0] == "!" :
            raise ValidationError("Not a valid title")

        if len(field.data.split()) < 1:
            raise ValidationError("Not a valid title")

        if field.data[0] == "." :
            raise ValidationError("Not a valid title")


#######################
###### VIEW FXNS ######
#######################

# @app.route('/')
# def home():
#     form = NameForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
#     if form.validate_on_submit():
#         name = form.name.data
#         newname = Name(name)
#         db.session.add(newname)
#         db.session.commit()
#         return redirect(url_for('all_names'))
#     return render_template('base.html',form=form)

@app.route('/names')
def all_names():
    names = Name.query.all()
    return render_template('name_example.html', names=names)

###################################
##### Routes & view functions #####
###################################

## Error handling routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


## Initialize form 

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TitleIdForm()
    if form.validate_on_submit():
        movie_titles = form.titles.data
        movie_directors = form.directors.data
        simpleForm = TitleIdForm()
    return render_template('base.html',form = form)

@app.route('/all_ids')
def see_all_ids():
    form = TitleIdForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        id_number = form.id_number.data
        SimpleForm = TitleIdForm()

    return render_template('all_ids.html',form=form)

@app.route('/all_titles', methods = ['GET'])
def see_all_titles():
    if request.method == 'GET':
        result = request.args['title']
        url = requests.get('http://www.omdbapi.com/?i=tt3896198&apikey=39a2a4a6?t='+result) 
    return render_template('all_titles.html',titles = Title.query.all() )


if __name__ == '__main__':
    db.create_all() # Will create any defined models when you run the application
    app.run(use_reloader=True,debug=True) # The usual

## Code to run the application...

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
