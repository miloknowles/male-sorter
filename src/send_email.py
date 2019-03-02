import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def SendEmail(receiver_email, text):
  try:
    # TODO: don't hardcore these
    sender_email = "biggerdata2019@gmail.com"
    password = 'bigdata1234'

    message = MIMEMultipart("alternative")
    message["Subject"] = "You've got mail!"
    message["From"] = "Automated Mail Services"
    message["To"] = receiver_email

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(sender_email, receiver_email, message.as_string())

  except:
    print('There was a problem sending mail to: %s' % receiver_email)
    return False

  return True

if __name__ == '__main__':
  receiver_email = "milokhl@gmail.com"
  text = """\
  Your mail was just dropped off! Come pick it up when you get a chance."""
  SendEmail(receiver_email, text)
