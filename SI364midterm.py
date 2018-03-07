###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required, Length # Here, too
from flask_sqlalchemy import SQLAlchemy
import omdb 
from flask_script import Manager 

## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/kaylawiSI364midterm"

## All app.config values

app.config['SECRET_KEY'] = 'API_info.key'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up Flask debug stuff

manager = Manager(app)

## Statements for db setup (and manager setup if using Manager)

db = SQLAlchemy(app) # For database use 


######################################
######## HELPER FXNS (If any) ########
######################################




##################
##### MODELS #####
##################

## Set up association Table between Director and Title Finish it later ##


class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280))
    director = db.Column(db.String(64))

    def __repr__(self):
        return "{0} (ID: {1})". format(self.text,self.id)


class Title(db.Model):
    __tablename__ = "titles"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64))
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    directors = db.relationship('Director', backref = 'Title') # This shows relationship between directors and titles 

    def __repr__(self):
        return "{0} (ID: {1})".format(self.title, self.id)


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

class DirectorTitleForm(FlaskForm):
    title_name = StringField("Enter the name of the movie: ", validators=[Required(),Length(min=1,max=280)])
    director_name = StringField("Enter the name of the director: ", validators=[Required(),Length(min=1,max=280)])
    submit = SubmitField('Submit')

    ## Custom Validation 


    def validate_title(self,field):

        if field.data[0] == "@" :
            raise ValidationError("Not a valid title")

        if field.data[0] == "!" :
            raise ValidationError("Not a valid title")

        if len(field.data.split()) < 1:
            raise ValidationError("Not a valid title")

        if field.data[0] == "." :
            raise ValidationError("Not a valid title")


    def validate_name(self,field):

        if field.data[0] == "@":
            raise ValidationError("Not a valid name")
       
        if len(field.data.split()) < 1: 
            raise ValidationError("Not a valid name")

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


@app.route('/', methods=['GET','POST'])
def index():
    form = DirectorTitleForm()

    # Find out if there's already a director with the entered name
    # if there is, save it in a variable: director
    # If not, then create one and add it to the database 

    d = Director.query.filter_by(directorname = director_name).first()
    if d:
        director = d
    else: 
        d = Director(directorname=director_name)  #addmore 
        db.session.add(d)
        db.session.commit()

    # If director already exist in database with this name
    # Then flash a message about the name already existing
    # And redirect to the list of directors 

    t = Title.query.filter_by(directorname = director_name, director_id = d.id).first() ## need to edit 
    if t:
        flash("Director exists")
        return redirect(url_for("  ")) ## need to create templates

    ## Render the template all_titles.html

    @app.route('/all_directors')
    def see_all_directors():
        all_directors = Director.query.all() 
        return render_template('all_directors.html') ## Complete this section 


    ## Render the template all_directors.html

    @app.route('all_titles')
    def see_all_titles():
        all_titles = Title.query.all()

        return render_template('all_titles.html') ## Complete this section

if __name__ == '__main__':
    db.create_all() # Will create any defined models when you run the application
    app.run(use_reloader=True,debug=True) # The usual

## Code to run the application...

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
