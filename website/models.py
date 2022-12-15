from . import db

class User(db.Model):
    # Added on init (in /description)
    id = db.Column(db.Integer, primary_key=True)
    seed = db.Column(db.Integer)
    guid = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    english = db.Column(db.Integer)
    time_created = db.Column(db.String(100))

    # Relationship (one-to-many) to Ratings
    ratings = db.relationship('Rating')
    # Relationship (one-to-many) to Ratings
    submit = db.relationship('Submit')

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_added = db.Column(db.String(100))
    imageid = db.Column(db.Integer)

    real = db.Column(db.Integer)
    humanlike = db.Column(db.Integer)
    eerie = db.Column(db.Integer)
    unsettling = db.Column(db.Integer)
    creepy = db.Column(db.Integer)
    hairraising = db.Column(db.Integer)
    friendly = db.Column(db.Integer)
    cheerful = db.Column(db.Integer)
    warmhearted = db.Column(db.Integer)
    
    # Relationship to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.guid'))

class Submit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Added one submitting (in /end)
    expertise = db.Column(db.Integer)
    experience = db.Column(db.Integer)
    uncanny_valley = db.Column(db.Integer)
    time_submitted = db.Column(db.String(100))
    familiarity = db.Column(db.Integer)
    # Relationship to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
