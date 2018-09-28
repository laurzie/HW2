## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################




####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def artist_form():
    return render_template('artistform.html')

@app.route('/artistinfo', methods = ['GET'])
def artist_info():
    if request.method == 'GET':
        artist = request.args.get("artist")
        print(artist)
    print("********")
    baseurl = "https://itunes.apple.com/search"
    params_diction = {}
    params_diction['term'] = artist
    response = requests.get(baseurl, params= params_diction)
    text = response.text
    python_obj = json.loads(text)
    response_py = python_obj["results"]
    return render_template('artist_info.html', objects = response_py)

@app.route('/artistlinks')
def artist_links():
    return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def artist_songs(artist_name):
    baseurl = "https://itunes.apple.com/search"
    params_diction = {}
    params_diction['term'] = artist_name
    response = requests.get(baseurl, params= params_diction)
    text = response.text
    python_obj = json.loads(text)
    print(python_obj)
    response_py = python_obj["results"]
    return render_template('specific_artist.html', results = response_py)

class AlbumEntryForm(FlaskForm):
    album_name = StringField('Enter the name of an album?', validators=[Required()])
    album_rating = RadioField('How much do you like this album? (1 low, 3 high)', choices = [('1', '1'), ('2','2'),('3','3')], validators = [Required()])
    submit = SubmitField('Submit')

@app.route('/album_entry')
def album_form():
    simple_album_Form = AlbumEntryForm()
    return render_template('album_entry.html', form=simple_album_Form)

@app.route('/album_result', methods = ['GET', 'POST'])
def album_results():
    form = AlbumEntryForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        recieved_album_name = form.album_name.data
        recieved_album_rating = form.album_rating.data
    print(recieved_album_rating)
    return render_template('album_data.html', name=recieved_album_name, rating = recieved_album_rating)

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
