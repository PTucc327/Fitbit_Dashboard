from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import webbrowser
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Replace with your own
CLIENT_ID = 'ENETER_CLIENT_ID_HERE'
CLIENT_SECRET = 'ENTER_CLIENT_SECRET_HERE'
REDIRECT_URI = 'http://127.0.0.1:8080/'

# Fitbit OAuth URLs
AUTH_BASE_URL = 'https://www.fitbit.com/oauth2/authorize'
TOKEN_URL = 'https://api.fitbit.com/oauth2/token'
SCOPE = ['activity', 'sleep', 'heartrate', 'profile']

# Step 1: Get authorization URL
fitbit = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
authorization_url, state = fitbit.authorization_url(AUTH_BASE_URL)

print("Go to the following URL and authorize access:")
print(authorization_url)

# Automatically open browser
webbrowser.open(authorization_url)

# Step 2: After authorizing, Fitbit will redirect to your redirect URI
# Copy the full URL from the browser after login (e.g. http://127.0.0.1:8080/?code=XYZ)

redirect_response = input("\nPaste the full redirect URL here:\n")

# Step 3: Fetch the access token
token = fitbit.fetch_token(
    TOKEN_URL,
    authorization_response=redirect_response,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
)

print("\n✅ Access token acquired!")
print("Access Token:", token['access_token'])
print("Refresh Token:", token['refresh_token'])
