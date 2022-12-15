from flask import Blueprint, render_template, redirect, url_for, send_from_directory, request, current_app, make_response
from .models import User, Rating, Submit
from . import db, CATALOGUE_NAME

from datetime import datetime, timedelta
import json, jwt, uuid, random, sys

views = Blueprint('views', __name__)

STOP_AFTER = 20
DO_MORE = 5
STR_FORMAT = "%m/%d/%Y-%H:%M:%S"
TOO_OLD = 2 # hours


with open("instance/"+CATALOGUE_NAME, "r") as infile:
    catalogue = json.load(infile)
    max = catalogue['last']

def get_image_id(seed, i):
    random.seed(seed)
    possible_ids = list(range(max))
    random.shuffle(possible_ids)
    return possible_ids[i]

def get_imagefile(i):
    return catalogue[str(i)]['filepath'].replace('website/','')

def set_token(resp,data):
    token = jwt.encode(data, current_app.config['SECRET_KEY'])
    resp.set_cookie('token', token)
    return resp

@views.route('/')
def home():
    return render_template("home.html")

## Description page containing info on what the questionaire is about
# This page contains the form that creates the users
@views.route('/description', methods=['GET', 'POST'])
def description():
    if request.method == 'POST':
        # Read data from form
        age = request.form.get('age')
        gender = request.form.get('gender')
        english = request.form.get('english')

        # make guid
        guid = str(uuid.uuid1())
        seed = random.randint(0, 10000000)

        # Add user to db
        new_user = User(guid = guid,
                        seed = seed,
                        age = age,
                        gender = gender,
                        english = english,
                        time_created = datetime.now().strftime(STR_FORMAT))        
        db.session.add(new_user)
        db.session.commit()

        # Create token for user
        token = jwt.encode({'u': guid,
                            'i' : 0,
                            'seed' : seed,
                            'stopafter' : STOP_AFTER,
                            'exp' : datetime.utcnow() + timedelta(hours=TOO_OLD)},
                            current_app.config['SECRET_KEY'])
        response = redirect(url_for('views.questions'))
        response.set_cookie('token', token)
        return response
    
    return render_template("description.html")


## Question page containing and image and the form to fill out
@views.route('/questions', methods=['GET', 'POST'])
def questions():

    # Handle token
    token = request.cookies.get('token')
    if token == None:
        print("No token found", file=sys.stdout)
        return redirect(url_for('views.home'))
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
    except jwt.exceptions.InvalidSignatureError:
        print("Token invalid", file=sys.stdout)
        return redirect(url_for('views.home'))

    img_id = get_image_id(data['seed'], data['i'])

    if request.method == 'POST':
        real        = int(request.form.get("real"))
        humanlike   = int(request.form.get("humanlike"))
        eerie       = int(request.form.get("eerie"))
        unsettling  = int(request.form.get("unsettling"))
        creepy      = int(request.form.get("creepy"))
        hairraising = int(request.form.get("hairraising"))
        friendly    = int(request.form.get("friendly"))
        cheerful    = int(request.form.get("cheerful"))
        warmhearted = int(request.form.get("warmhearted"))
        
        new_rating = Rating(real        = real,
                            humanlike   = humanlike,
                            eerie       = eerie,
                            unsettling  = unsettling,
                            creepy      = creepy,
                            hairraising = hairraising,
                            friendly    = friendly,
                            cheerful    = cheerful,
                            warmhearted = warmhearted,
                            user_id     = data['u'],
                            time_added  = datetime.now().strftime(STR_FORMAT),
                            imageid     = img_id)
        db.session.add(new_rating)
        db.session.commit()

        # Increment image counter
        data['i'] = data['i'] + 1
    
    # Make new token
    new_token = jwt.encode(data, current_app.config['SECRET_KEY'])
    
    # Check for end of questionnaire logic here
    if data['i'] == data['stopafter']:
        response = redirect(url_for('views.intermediate'))
        response.set_cookie('token', new_token)
        return response

    new_id = get_image_id(data['seed'], data['i'])
    img_file = get_imagefile(new_id)

    response = make_response(render_template("questions.html", imgfile=img_file))
    response.set_cookie('token', new_token)
    return response

## Question page containing and image and the form to fill out
@views.route('/intermediate', methods=['GET', 'POST'])
def intermediate():
    # Handle token
    token = request.cookies.get('token')
    if token == None:
        print("No token found", file=sys.stdout)
        return redirect(url_for('views.home'))
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
    except jwt.exceptions.InvalidSignatureError:
        print("Token invalid", file=sys.stdout)
        return redirect(url_for('views.home'))
    # Handle token end

    if request.method == 'POST':
        if request.form['action'] == 'more':
            response = redirect(url_for('views.questions'))
            data['stopafter'] = data['stopafter'] + DO_MORE
            new_token = jwt.encode(data, current_app.config['SECRET_KEY'])
            response.set_cookie('token', new_token)
            return response
        elif request.form['action'] == 'end':
            return redirect(url_for('views.end'))
    else:
        return render_template("intermediate.html")

@views.route('/end', methods=['GET', 'POST'])
def end():
    # Handle token
    token = request.cookies.get('token')
    if token == None:
        print("No token found", file=sys.stdout)
        return redirect(url_for('views.home'))
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
    except jwt.exceptions.InvalidSignatureError:
        print("Token invalid", file=sys.stdout)
        return redirect(url_for('views.home'))
    # Handle token end

    if request.method == 'POST':
        # Read data from form
        experience = request.form.get('animation_experience')
        expertise = request.form.get('animation_expert')
        uncanny_valley = request.form.get('uncanny_valley')
        familiarity = request.form.get('familiarity')
        # Find user to update and update cols
        new_submit = Submit(experience     = experience,
                            expertise      = expertise,
                            uncanny_valley = uncanny_valley,
                            familiarity    = familiarity,
                            user_id        = data['u'],
                            time_submitted = datetime.now().strftime(STR_FORMAT))       
        db.session.add(new_submit)
        db.session.commit()
        return redirect(url_for('views.home'))
    else:
        return render_template("end.html")

@views.route('/favicon.ico')
def favicon():
    return send_from_directory('static/','images/favicon.png')