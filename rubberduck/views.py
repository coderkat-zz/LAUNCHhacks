from rubberduck import app
import keepitsecret
from firebase import firebase
from flask import request, render_template, redirect
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
        import pdb; pdb.set_trace()
        # query for user by access token within stored users:
        # user = firebase.get('/users', access_token)
        # if user:
            # if found, log in to app if user has checked in within the last 3 hours
            # double-check that you're at the location we think you're at...
            # if not checked in, prompt to check in with 4sq before accessing site for help
            # pass
        # else:
        # create a new user object
        new_user = access_token
        user = firebase.post('/users', new_user)

        print user

        # return redirect(auth_uri)

        # prompt user for foursquare oauth
        # write whatever data we need(???) to firebase
        # sent user to codesocial page
        # return render_template('codesocial.html')



@app.route('/codesocial')
def codesocial():
    
    # query_string = request.query_string

    # access_token = client.oauth.get_token(query_string[5:])
    # # Apply the returned access token to the client
    # client.set_access_token(access_token)
    # # Get the user's data
    # user = client.users()
    # print user
    # find user in firebase, append fsq token data to user object
    # firebase.post('users/%s/' % (user_name))
    # view how many users are checked in to your location
    return render_template('codesocial.html')
