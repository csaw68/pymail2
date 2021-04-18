# import required packages
from email.mime.text import MIMEText
import base64
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient import errors
import time

# command to install new packages (if applicable)
# conda install pickle
# conda install google_auth_oauthlib
# uses conda-forge because it's not officially within conda's own server
# conda install -c conda-forge google-api-python-client

def create_message(sender, to, subject, message_text):
#   Create a message for an email.
# Args:
#     sender: Email address of the sender.
#     to: Email address of the receiver.
#     subject: The subject of the email message.
#     message_text: The text of the email message.
# Returns:
#     An object containing a base64url encoded email object.
#   
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(service,user_id,message):
#   Send an email message.

#   Args:
#     service: Authorized Gmail API service instance.
#     user_id: User's email address. 
#     message: Message to be sent.

#   Returns:
#     Sent Message.
#
    timestamp = time.ctime(time.time())
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print ('Message Successfully Sent!')
        print (timestamp)
#        print ('Message Id: %s' % message['id'])
#        return message
        return None
    except errors.HttpError as error:
        print ('An error occurred: %s' % error)

def service_account_login():
# give user access to send email from Gmail by authentication
# uses generated .json file to access Gmail API,
# authenticates user, then get access to Gmail services
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        # We use login if no valid credentials
    SCOPES = 'https://mail.google.com/'

    if not creds or not creds.valid:
 #       if creds and creds.expired and creds.refresh_token:
        flow =   InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service






        
