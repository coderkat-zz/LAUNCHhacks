from rubberduck import app
import keepitsecret
from firebase import firebase
from flask import request, render_template, redirect
import foursquare

firebase = firebase.FirebaseApplication('https://hacksocial.firebaseio.com/', None)

# foursquare client auth info
client = foursquare.Foursquare(client_id=keepitsecret.foursquare_client_id,
                               client_secret=keepitsecret.foursquare_client_secret,
                               redirect_uri='localhost:5000/')
# Build the authorization url for your app
auth_uri = "https://foursquare.com/oauth2/authorize?client_id="+keepitsecret.foursquare_client_id+"&response_type=token&redirect_uri=http://localhost:5000/"


@app.route('/index', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # query for user within stored users:
            # if found, log in to app if user has checked in within the last 3 hours
            # double-check that you're at the location we think you're at...
            # if not checked in, prompt to check in with 4sq before accessing site for help
        # if none is found:
        # create a new user object
        new_user = request.form['text']
        result = firebase.post('/users', new_user)
        print result
        return redirect(auth_uri)

        # prompt user for foursquare oauth
        # write whatever data we need(???) to firebase
        # sent user to codesocial page
        # return render_template('codesocial.html')



@app.route('/codesocial')
def codesocial():
    # view how many users are checked in to your location
    return render_template('codesocial.html')
