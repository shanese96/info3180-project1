from app import app, forms, db
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.models import Profile as Profile
from glob import glob

import os
import re
import datetime

# Route for application
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route('/profile', methods=('GET','POST'))
def profile():
    """Render the website's add profile page."""
    form = forms.ProfileForm()
    if request.method() == 'POST':
        if form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            location = form.location.data
            gender = form.gender.data
            biography = form.biography.data
            
            photo = form.photo.data
            filename = secure_filename(photo.filename)
            
            
            if not re.match(r'.*\.(jpg|png|jpeg)$', filename):
                flash("Invalid file. File must have .jpg/.png/.jpeg extension")
                flash_errors(form)
                return render_template('profile.html', form = form)
            
            profile = Profile(firstname, lastname, email, location, gender,
                        biography, created_on=date_joined())
            
            db.session.add(profile)
            db.session.commit()
            
            form.save(os.path.join(app.config['UPLOAD_FOLDER'], 
                      str(profile.id) + "_" + filename))
            
            flash("Profile successfully created")
            return redirect(url_for('profiles'))
        
        flash_errors(form)
        return render_template('profile.html', form=form)


@app.route('/profiles', defaults={'userid': None})
@app.route('/profiles/<userid>')
def profiles(userid):
    """Render the website's profiles page."""
    if not userid:
        profiles = [(profile.id, find_photo(profile.id), profile.firstname, profile.lastname, 
        profile.gender, profile.location) for profile in db.session.query(Profile).all()]
        return render_template('profiles.html', profiles=profiles)
    else:
        try:
            user = db.session.query(Profile).filter_by(id=userid).first()
        
            return render_template('details.html', name=user.firstname + " " + user.lastname,
                   email=user.email, location=user.location, bio=user.biography, 
                   photo=find_photo(user.id),  registered=user.joined_.strftime('%B %d, %Y'))
        
        except:
            return render_template("404.html")
    

def date_joined():
    date = datetime.datetime.now()
    return date.strftime("%B %d, %Y")


def find_photo(uniqueid):
    file = glob(os.path.join(app.config['UPLOAD_FOLDER'], 
            str(uniqueid) + "_*"))[0]
    print(file[file.index("profiles"):])
    return file[file.index("profiles"):]


##Code retrieved from Mr Yannick Lynfatt (lab demonstration)
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error), 'danger')


##Code retrieved from Mr Yannick Lynfatt (previous labs)
@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


##Code retrieved from Mr Yannick Lynfatt (previous labs)
@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


##Code retrieved from Mr Yannick Lynfatt (previous labs)
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")