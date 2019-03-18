from . import db

class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    location = db.Column(db.String(40))
    biography = db.Column(db.String)
    gender = db.Column(db.String)
    joined_on = db.Column(db.DateTime)
    
    
    def __repr__(self):
        return '<Profile id={} firstname={} lastname={} email={} location={} gender={}\nbio={}>'.format(
            self.id, self.firstname, self.lastname, self.email, self.location, self.gender, self.biography)