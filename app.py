from flask import Flask, render_template, jsonify, g
import locale
from decimal import Decimal

locale.setlocale(locale.LC_ALL, '')

app = Flask(__name__)

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
   {"name": "game dev", "rate_us_per_hour": 34.11, "tags": "puzzle games, RPG, edutainment, research, mobile devices", "faicon": "fa fa-gamepad"},
   {"name": "database", "rate_us_per_hour": 21.13, "tags": "data design, implementation, standards, security, authorization, authentication, distribution, production, maintenance", "faicon": "fa fa-database"},
   {"name": "macros", "rate_us_per_hour": 21.13, "tags": "Microsoft, simple, small, focused, Office, solutions, unique problems", "faicon": "fa fa-code-fork"},
   {"name": "software dev", "rate_us_per_hour": 32.10, "tags": "Linux, MacOS, Windows, standalone, efficient, portable, connectivity", "faicon": "fa fa-floppy-o"},
   {"name": "image dev", "rate_us_per_hour": 25.00, "tags": "logos, splashes, screensavers, background images, posters, AI prompter, JPEG, PNG, GIF, animated GIF, RGB, RGBY", "faicon": "fa fa-picture-o"}
]
# end of global area space

# localized user-defined function to format the currency accordingly
def format_currency(value):
    # Convert the value to Decimal for accurate monetary computations
    decimal_value = Decimal(value)
    # Format the decimal value as currency
    currency_string = locale.currency(decimal_value, grouping=True)
    return currency_string

# register created functions for utilization by other objects
@app.context_processor
def utility_processor():
    return dict(setcurrency=format_currency)

# things to do just before any request is handled
@app.before_request
def before_request():
   g.cnv_usd_to_jmd = cnv_usd_to_jmd
   g.order_by = order_by

# setting up all routes for the web system solution
@app.route('/')
def home():
   return render_template("index.html", services=services)

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

@app.route('/aboutus')
def aboutus():
   return render_template("about.html")

# handling errors from the server before they go to the client as a response
@app.errorhandler(404)
def resourceNotFound(e):
   return render_template("index.html", services=services)

# main preprocessing directives
if __name__ == '__main__':
   app.run(debug=True)
