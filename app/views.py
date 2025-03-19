from app import app, db, login_manager
import os
import locale
import random
import string
from datetime import datetime
from decimal import Decimal
from sqlalchemy.sql import func
from flask import Flask, render_template, request, redirect, url_for, g, flash, abort, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from .forms import StaffRateForm, FeedbackForm, LoginForm, csrf
from .models import Feedbacks, User, StaffRating
from .config import Config
from is_safe_url import is_safe_url
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import json
import matplotlib.pyplot as plt

locale.setlocale(locale.LC_ALL, '')

# global variable space
cnv_usd_to_jmd = 172.03
order_by = [
   {"name": "Title", "code": 'name'},
   {"name": "Cost", "code": 'rate_us_per_hour'},
   {"name": "Tags", "code": 'tags'}
]
services = [
   {"name": "BI", "rate_us_per_hour": 25.45, "tags": "dashboard design, data mining, big data, crowd-sourcing, data analytics, heuristic inferences, projections", "faicon": "fa fa-briefcase"},
   {"name": "mobile app dev", "rate_us_per_hour": 45.51, "tags": "Android, iOS, Blackberry, Windows Phone, responsive, multi-platform, native coding, AI-inclusion, augmented reality", "faicon": "fa fa-mobile"},
   {"name": "VR dev", "rate_us_per_hour": 41.22, "tags": "mobile devices, 3D audio, touch, secure, efficiency, optimality, fun", "faicon": "fa fa-random"},
   {"name": "game dev", "rate_us_per_hour": 37.71, "tags": "puzzle games, RPG, edutainment, research, mobile devices", "faicon": "fa fa-gamepad"},
   {"name": "database", "rate_us_per_hour": 21.13, "tags": "data design, implementation, standards, security, authorization, authentication, distribution, production, maintenance", "faicon": "fa fa-database"},
   {"name": "macros", "rate_us_per_hour": 21.13, "tags": "Microsoft, simple, small, focused, Office, solutions, unique problems", "faicon": "fa fa-code-fork"},
   {"name": "software dev", "rate_us_per_hour": 32.10, "tags": "Linux, MacOS, Windows, standalone, efficient, portable, connectivity", "faicon": "fa fa-floppy-o"},
   {"name": "image dev", "rate_us_per_hour": 25.00, "tags": "logos, splashes, screensavers, background images, posters, AI prompter, JPEG, PNG, GIF, animated GIF, RGB, RGBY", "faicon": "fa fa-picture-o"}
]
objNow = datetime.now()
# end of global area space

# register created functions for utilization by other objects
@app.context_processor
def utility_processor():
    return dict(setcurrency=format_currency)

# things to do just before any request is handled
@app.before_request
def before_request():
   g.cnv_usd_to_jmd = cnv_usd_to_jmd
   g.order_by = order_by
   g.strCurrentDateTime = ( (f' | {objNow.strftime("%A, %B %d, %Y %I:%M:%S %p")}') if app.config['SHOW_FOOTER_DATE']=='True' else '.')
   g.imageloc = get_stock_jpeg()

# setting up all routes for the web system solution
@app.route('/')
def home():
   # user = User ('lileitch', 'laurie.leitch@uwimona.edu.jm', 'LILeitch', 'blueford')
   # db.session.add(user)
   # db.session.commit()
   #user = User ('goldbane@yahoo.com', 'li.leitch@utechjamaica.edu', 'Laurie I. Leitch', 'greenford')
   #db.session.add(user)
   #db.session.commit()
   return render_template("index.html", services=services)

# section that allows for authorization of specific users
@app.route('/login', methods=['GET', 'POST'])
def login():
   if current_user.is_authenticated:
      # redirect user to special user page if they are already logged in
      return redirect(url_for('secure_page'))

   # set up the form for data entry and validation purposes
   form = LoginForm()
   # Login and validate the user.
   if form.validate_on_submit():
      username = form.username.data
      password = form.password.data

      # Check to see if username and password exists in the system
      user = db.session.execute(db.select(User).filter_by(username=username)).scalar()

      if user is not None and check_password_hash(user.password, password):
         remember_me = False

         if 'remember_me' in request.form:
            remember_me = True

         # log the user in based on their user details and remember me state
         login_user(user, remember=remember_me)

         flash ('Logged in successfully.', 'success')

         next_page = request.args.get('next')

         # load the next internal space if it is safe to do so
         if not is_safe_url(next_page, request.host):
            return abort(400)

         return redirect(next_page or url_for('home'))
      else:
         flash ('Username or Password is incorrect.', 'danger')

   flash_errors (form)
   return render_template('login.html', form=form)

# space that allows authenticated users to rate staff members
@app.route('/staff-rating', methods=['GET', 'POST'])
@login_required
def staff_rating():
   lstratevals = [8, 5, 3, 2, 1]
   # set up form and validation after receiving contents
   stfform = StaffRateForm()

   if stfform.validate_on_submit():
      data = stfform.staff_rating.data

      if data:
         try:
            # load the contents of the staff rating from the request to the database
            lstStaff = json.loads(data)

            i = 0
            for staff in lstStaff:
               if staff:
                  staff_name = staff.replace('"','').replace('-',' ')
                  rating = StaffRating (current_user.id, staff_name, lstratevals[i])
                  db.session.add(rating)
                  i += 1

            db.session.commit()

         except json.JSONDecodeError as e:
            print("JSON Decode Error:", e)

      else:
         print("No data to decode")

   # get all of the image filenames in the workers directory and store to an array
   workers_dir = os.path.join(app.static_folder, 'images/workers')
   image_files = [
     f for f in os.listdir(workers_dir)
   ]

   # get stored ratings from the database grouped by staff names
   lst_staff = []
   lst_scores = []
   results = db.session.query(
      StaffRating.rated_name,
      func.sum(StaffRating.rated_value).label('total_rating')
   ).group_by(StaffRating.rated_name).all()

   for staff_name, total in results:
      lst_staff.append(staff_name)
      lst_scores.append(total)

   # generate a frequency graph/chart based on the contents from the database
   plt.figure(figsize=(10, 6))
   plt.bar(lst_staff, lst_scores, color='deeppink')
   plt.title('Current Staff Rating')
   plt.xlabel('Staff', fontsize=12)
   plt.ylabel('Rating', fontsize=12)
   plt.xticks(fontsize=10)

   # Save the figure as a PNG file
   str_chart_file = ('src-' + generate_random_filename(24) + '.png')
   chart_path = ('app/static/images/charts/' + str_chart_file)
   plt.savefig(chart_path)
   plt.close()  # Close the figure to free memory

   return render_template('staff_rating.html', stfform=stfform, image_files=image_files, csrf_token=csrf.generate_csrf(), chart_url=str_chart_file)

# a unique space for those authenticated users
@app.route('/auth-dashboard')
@login_required
def secure_page():
   lst_stats = []
   # connect to database and get list of feedback in the database
   # get the full count of all feedback in the system
   num_total = db.session.query(Feedbacks).count()
   lst_stats.append({'descript': 'The total number of Feedback Messages to-date', 'value': num_total})
   # get the number of unique emails sent by those giving feedback
   num_profs = db.session.query(Feedbacks).filter(Feedbacks.title.ilike('%Prof%')).count()
   lst_stats.append({'descript': 'The total number of Professor messages to-date', 'value': num_profs})
   # get the full count of doctor feedback from the system
   num_docs = db.session.query(Feedbacks).filter(Feedbacks.title.ilike('%Dr%')).count()
   lst_stats.append({'descript': 'The total number of Doctor messages to-date', 'value': num_docs})
   # get the full count of web app dev feedback from the system
   num_webs = db.session.query(Feedbacks).filter(Feedbacks.area_interest.ilike('%Web App%')).count()
   lst_stats.append({'descript': 'The total number of Web App Dev messages to-date', 'value': num_webs})
   # get the full count of software dev feedback from the system
   num_soft = db.session.query(Feedbacks).filter(Feedbacks.area_interest.ilike('%Software%')).count()
   lst_stats.append({'descript': 'The total number of Software Dev messages to-date', 'value': num_soft})

   return render_template('auth_dashboard.html', lst_stats=lst_stats)

@app.route("/logout")
@login_required
def logout():
   # Logout the user and end the session
   logout_user()
   flash('You have been logged out.', 'success')
   return redirect(url_for('home'))

# the statistical view based on feedback contents
@app.route('/feedback/stats')
def feedback_statistics():
   lst_stats = []
   # connect to database and get list of feedback in the database
   # get the full count of all feedback in the system
   num_total = db.session.query(Feedbacks).count()
   lst_stats.append({'descript': 'The total number of Feedback Messages to-date', 'value': num_total})
   # get the number of unique emails sent by those giving feedback
   num_profs = db.session.query(Feedbacks).filter(Feedbacks.title.ilike('%Prof%')).count()
   lst_stats.append({'descript': 'The total number of Professor messages to-date', 'value': num_profs})

   return render_template("feedback_stats.html", lst_stats=lst_stats)

# for loading the front page with a specific service ordering in place
@app.route("/<servorder>/<orderdir>")
def home_services_order(servorder, orderdir):
   # check values that are coming in to see if they are legit
   if (orderdir != 'asc' and orderdir != 'dsc'):
      return render_template("index.html", services=services)
   elif (not any(order.get('code') == servorder for order in order_by)):
      return render_template("index.html", services=services)
   # perform the ordering of the values before rendering same
   sortedlist = sorted(services, key=lambda service: service[servorder], reverse=(orderdir == 'dsc'))
   return render_template("index.html", services=sortedlist, servorder=servorder, orderdir=orderdir)

# for loading the About Us section of the web space
@app.route('/aboutus')
def aboutus():
   return render_template("about.html")

# for loading the feedback area to get responses from the web space users
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
   fbForm = FeedbackForm()
   if fbForm.validate_on_submit():
      # process the received form data for presenting back to the client
      email = fbForm.email.data
      selected_title = fbForm.title.data
      selected_service_preference = fbForm.service_preference.data
      areas_interest = [
         ('Mobile Dev' if fbForm.area_interest_1.data else ''), 
         ('Software Dev' if fbForm.area_interest_2.data else ''), 
         ('Web App Dev' if fbForm.area_interest_3.data else '')]
      subject = fbForm.subject.data
      message = fbForm.message.data
      if request.method == "POST":
         fdback = Feedbacks(
            email, 
            selected_title, 
            selected_service_preference, 
            areas_interest, 
            subject, 
            message)
         db.session.add(fdback)
         db.session.commit()
         flash(f'New Feedback from {email} was successfully added to the db')
      else:
         # show flash notification of success, then return template with contents
         flash(f'Feedback received from {email}!', 'success')

      return render_template('feedback.html', fbForm=fbForm, email=email)
   else:
      # Inspect and flash form errors
      for fieldName, errorMessages in fbForm.errors.items():
         for err in errorMessages:
            flash(f"Error in {fieldName}: {err}", 'danger')

   # ensure to display the default form based on the details in the class FeedbackForm
   return render_template('feedback.html', fbForm=fbForm)

# simple feedback received page that shows all contents sent
@app.route('/feedback/received')
def feedback_received():
    email = request.args.get('email', 'guest@lelaiv.com')
    return f"Received feedback from {email}"

# main preprocessing directives
if __name__ == '__main__':
   app.run(debug=True)

# localized user-defined function to format the currency accordingly
def format_currency(value):
    # Convert the value to Decimal for accurate monetary computations
    decimal_value = Decimal(value)
    # Format the decimal value as currency
    currency_string = locale.currency(decimal_value, grouping=True)
    return currency_string

# return the string of a random JPEG stock photo to be displayed
def get_stock_jpeg():
   strRetn = url_for('static', filename='images/favicon.ico')
   # get all of the images filenames in the directory and store to an array
   images_dir = os.path.join(app.static_folder, 'images')
   image_files = [
     f for f in os.listdir(images_dir) if f.endswith(('-stock-office.jpeg'))
   ]
   # get and return a random image filename string
   if len(image_files) > 0:
      strRetn = image_files[random.randrange(len(image_files))]
   return strRetn

# This callback is used to reload the user object from the user ID stored in the session.
# It should take the unicode ID of a user, and return the corresponding user object.
@login_manager.user_loader
def load_user(id):
   return db.session.execute(db.select(User).filter_by(id=id)).scalar()

# generate a random filename-safe string based on parameter length provided
def generate_random_filename(length=10):
   # Define safe characters for filenames
   safe_characters = string.ascii_letters + string.digits + "_."

   # Generate a random string from the safe characters
   random_string = ''.join(random.choice(safe_characters) for _ in range(length))

   return random_string

# Flash errors from the form if validation fails with Flask-WTF
def flash_errors(form):
   for field, errors in form.errors.items():
      for error in errors:
         flash(u"Error in the %s field - %s" % (
            getattr(form, field).label.text,
            error
         ), 'danger')

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
   """Send your static text file."""
   file_dot_text = file_name + '.txt'
   return app.send_static_file(file_dot_text)

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

@app.errorhandler(404)
def page_not_found(error):
   """Custom 404 page."""
   return render_template('404.html'), 404