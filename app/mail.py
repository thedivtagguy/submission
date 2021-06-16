import os
import smtplib, ssl
from email.message import EmailMessage
from random import randint
from datetime import datetime 


def send_email(x, uid, y):    
    
    
    sender_email = "dwightbeatlesmichaelharry@gmail.com"
    
    receiver_email = x
    
    password = os.environ.get("EMAIL_PASS")
    
    msg = EmailMessage()
    
    # generic email headers
    msg['Subject'] = "Submission For " + y +  " Received!" #subjectline + ' | ' + date
    msg['From'] = 'Srishti Archive dwightbeatlesmichaelharry@gmail.com'
    msg['To'] = x
    
   
    
    # set an alternative html body
    msg.add_alternative("""\
    <html>
        <body style="background: #fff;font: 15px/24px; background-color: #ffffff; margin: 0; -webkit-font-smoothing: antialiased;font-smoothing: antialiased; max-width:500px; margin:auto; padding-top:10vh;">
        <div>
        <div style="text-align:center;">
            <img style="width:20%;" src="https://i.imgur.com/gvRNpAb.png">

        </div>
            <div class="message-body">
                <div class="digest" style="margin-bottom: 3rem;">
    
                    <p style="font-family: Menlo, Courier, Courier New, monospace; line-height: 1.25; font-size: 16px; margin: 0; margin-bottom: 1rem;">Hi!</p>
        
                </div>
    
                <div class="top-by-share" style="margin-bottom: 3rem;">
                    <p class="section-title" style="font-family: Menlo, Courier, Courier New, monospace; line-height: 1.25; font-size: 14px; margin: 0; padding-bottom:10px;">This is to let you know that your submission <strong>(ID: {entry_id})</strong> for your project <strong>{project}</strong> has been received and is now under manual review. If all the information required is entered correctly, it will be published later this week. <br><br>We'll notify you about the status by email.</p>
    
    
                    <div class="link" style="margin-bottom: 2rem;text-align: center;">
                    <img src="https://media.giphy.com/media/ZfK4cXKJTTay1Ava29/source.gif" style="padding:10px;">
    
                    </div>
                </div>
                <div class="promo" style="margin-bottom: 3rem;">
                    <p style="font-family: Menlo, Courier, Courier New, monospace; line-height: 1.25; font-size: 16px; margin: 0; margin-bottom: 1rem;">
                        You've helped add to a growing collection of Srishti projects, documented for future students. And that's very cool of you. Thanks.
                    </p>
    
                    <p style="font-family: Menlo, Courier, Courier New, monospace; line-height: 1.25; font-size: 16px; margin: 0; margin-bottom: 1rem;">Have a great week! (ʘ‿ʘ)╯</p>
                    <h6 style="padding-bottom:10px;font-size:8px;text-align:right;color:gray;">Acknowledgement for Submission ID {entry_id}</h6>

                </div>
            </div>
    
    
        </div>
    </body>
    </html>
    """.format(entry_id = uid,
                project = y), 
        subtype='html')
        
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, msg.as_string()
        )
        