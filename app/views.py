from app import app, db
import os
import locale
import random
from datetime import datetime
from decimal import Decimal
from flask import Flask, render_template, request, redirect, url_for, g, flash
from .forms import FeedbackForm  # Assuming forms.py contains FeedbackForm
from .models import Feedbacks
from .config import Config

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
   return render_template("index.html", services=services)

# the statistical view based on feedback contents
@app.route('/feedback/stats')
def feedback_statistics():
   lst_stats = []
   # connect to database and get list of feedback in the database
   # lst_feedback = db.session.execute(db.select(Feedbacks)).count()
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

# handling errors from the server before they go to the client as a response
@app.errorhandler(404)
def resourceNotFound(e):
   return render_template("index.html", services=services)

# main preprocessing directives
if __name__ == '__main__':
   app.run(debug=True)
