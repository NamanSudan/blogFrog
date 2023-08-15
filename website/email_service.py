# email_service.py

import sendgrid
from sendgrid.helpers.mail import *
import os  # Import the os module

# Load environment variable
from dotenv import load_dotenv
load_dotenv()

def send_email(to_email, subject, content):
    # Fetch the SendGrid API key from the environment variable
    SENDGRID_API_KEY = os.environ.get("SMTP_PASSWORD")
    
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    
    from_email = Email("namansudans@gmail.com")  
    to_email = To(to_email)  # This is where you specify the recipient's email
    content = Content("text/html", content)

    mail = Mail(from_email, to_email, subject, content)

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        if response.status_code not in [200, 201, 202]:  # Add this to print a warning if the response is anything other than success
            print("Warning: Email may not have been sent successfully.")
            print(response.body)
            print(response.headers)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("Error:", e)

