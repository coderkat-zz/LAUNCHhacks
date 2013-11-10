from rubberduck import app
import keepitsecret
from firebase import firebase
from flask import request, render_template, redirect, url_for, session
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired
import foursquare
import json
import time

firebase = firebase.FirebaseApplication('https://hacksocial.firebaseio.com/', authentication=None)

client_id = keepitsecret.foursquare_client_id
client_secret = keepitsecret.foursquare_client_secret
# foursquare client auth info
# client = foursquare.Foursquare(client_id=keepitsecret.foursquare_client_id,
#                                client_secret=keepitsecret.foursquare_client_secret,
#                                redirect_uri='localhost:5000/')
# # Build the authorization url for your app
auth_uri = "https://foursquare.com/oauth2/authenticate?client_id=" + client_id + "&response_type=code&redirect_uri=http://localhost:5000/codesocial"

@app.route('/')
def index():
    return redirect(url_for('sign_up'))


@app.route('/index', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        # or if this is a GET request with request.data, can we treat that as a form submission?
        return render_template('index.html', client_id=client_id, client_secret=client_secret)
    else:
        # handle POSTed data from foursquare
        request_data = json.loads(request.data)
        user_data = request_data['user_data']
        access_token = request_data['access_token']
        user_id = user_data['id']

        # query for user by id within stored users:
        user = firebase.get('/users', user_id)

        if user:
            session['user_id'] = user_data['id']
            # last_checkin = firebase.get('/users/%s' % (access_token), checkin)
            # what format is this checkin data in?
            # get timestamp of checkin.
            # do some math: was it less than 3 hours ago?
            # double-check that you're at the location we think you're at?
            # if so, consider user logged in already and start that floww
            # print last_checkin
            # if not checked in, prompt to check in with 4sq (is on a separate page) before accessing site for help
            # return redirect(url_for("codesocial"))
            return 'string'
        else:
            print('creating a new user object')
            # create a new user object
            user_name = user_data['firstName'] + " " + user_data['lastName']
            # put user data into firebase user objects
            user = firebase.put('/users', user_id, user_id)
            firebase.put('/users/%s' %(user), 'access_token', access_token)
            firebase.put('/users/%s' %(user), 'name', user_name)
            firebase.put('/users/%s' %(user), 'photo', user_data['photo'])
            # set up user w/3 karma points
            session['user_id'] = user_id

            return 'string'
            # redirect to some sort of user settings page
            # form inputs for (later: skills) and (now:MVP)phone number
            # submit form and send them to check-in reminder page
            # return redirect(url_for("codesocial"))
        return 'hey'


@app.route('/codesocial')
def codesocial():
    if 'user_id' in session:
        user_id = session['user_id']
        user = firebase.get('/users', user_id)
        has_phone = user.get('phone')
        print has_phone
        if has_phone == None:
            return render_template('userdata.html', user = user_id)
        else:
            # get location id of most recent check-in
            current_venue = firebase.get('/users/%s' % (user_id), 'lastcheckinvenueid')
            if not current_venue:
                # TODO: make this redirect to a 'waiting for you to check in' pattern/page
                return redirect(url_for('sign_up'))
            else:
                # get the dictionary of users whose last checkin was this venue {user_id:checkintime}
                users_at_venue = firebase.get('/venues/%s' % (current_venue), None)
                if users_at_venue:
                    users_count = len(users_at_venue.keys())
                    helper_phones = []
                    for key, value in users_at_venue.iteritems():
                        helper_phone = firebase.get('/users/%s' % (key), 'phone')
                        helper_phones.append(helper_phone)

                # calculate time since user's last checkin
                checkin_time = firebase.get('/users/%s' % (user_id), 'lastcheckintime')
                current_time = time.time()
                time_elapsed = current_time - checkin_time

                # check to see if it's been more than 3 hours since the last checkin
                if time_elapsed >= 10800:
                    # Ask user to check in if they're somewhere new?
                    check_checkin = True
                else:
                    check_checkin = False

                access_token = firebase.get('/users/%s' % (user_id), 'access_token')

                # pass that data to the template, use Jinja logic to decide what to render on the page...
                return render_template('codesocial.html',
                                        user = user,
                                        user_json=json.dumps(user),
                                        venue=current_venue,
                                        other_users=users_at_venue,
                                        helper_phones=map(json.dumps, helper_phones),
                                        check_checkin=check_checkin,
                                        users_count=users_count,
                                        access_token=access_token,
                                        )
    else:
        return redirect(url_for('sign_up'))

@app.route('/save_phone', methods=['POST'])
def save_phone():

    if request.method == 'POST':
        phone = request.form['phone_number']
        user_info = request.form['user']

        # user = firebase.get('/users', user_info)
        firebase.put('/users/%s' %(user_info), 'phone', phone)

        return redirect(url_for('codesocial'))



    return 'newurl'


@app.route('/helpisontheway')
def helpout():
        # helper is responding to request for help
        return render_template('helpisontheway.html')


app.secret_key = keepitsecret.flask_key
