from rubberduck import app
import keepitsecret
from firebase import firebase
from flask import request, render_template, redirect, url_for
# import foursquare
import json

firebase = firebase.FirebaseApplication('https://hacksocial.firebaseio.com/', authentication=None)

client_id = keepitsecret.foursquare_client_id
client_secret = keepitsecret.foursquare_client_secret
# foursquare client auth info
# client = foursquare.Foursquare(client_id=keepitsecret.foursquare_client_id,
#                                client_secret=keepitsecret.foursquare_client_secret,
#                                redirect_uri='localhost:5000/')
# # Build the authorization url for your app
auth_uri = "https://foursquare.com/oauth2/authenticate?client_id=" + client_id + "&response_type=code&redirect_uri=http://localhost:5000/codesocial"


@app.route('/index', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        return render_template('index.html', client_id=client_id, client_secret=client_secret)
    else:
        # handle POSTed data from foursquare
        request_data = json.loads(request.data)
        user_data = request_data['user_data']
        access_token = request_data['access_token']

        # query for user by access token within stored users:
        user = firebase.get('/users', access_token)
        if user:

            print user
            # last_checkin = firebase.get('/users/%s' % (access_token), checkin)
            # what format is this checkin data in?
            # get timestamp of checkin.
            # do some math: was it less than 3 hours ago?
            # double-check that you're at the location we think you're at?
            # if so, consider user logged in already and start that floww
            # print last_checkin
            # if not checked in, prompt to check in with 4sq (is on a separate page) before accessing site for help

        else:
            # create a new user object
            new_user = access_token
            user_name = user_data['firstName'] + " " + user_data['lastName']
            # put user data into firebase user object
            user = firebase.put('/users', new_user, new_user)
            firebase.put('/users/%s' %(user), 'name', user_name)
            firebase.put('/users/%s' %(user), 'photo', user_data['photo'])
            # set up user w/3 karma points
            print user
            # redirect to some sort of user settings page
            # form inputs for (later: skills) and (now:MVP)phone number
            # submit form and send them to check-in reminder page
        return redirect(url_for("codesocial"))



@app.route('/codesocial', methods=['GET'])
def codesocial():
    return render_template('codesocial.html')
