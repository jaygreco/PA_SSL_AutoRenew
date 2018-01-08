'''
A Python script to automatically renew LetsEncrypt SSL certificates on PythonAnywhere.
This code is supplied as-is; use at your own risk.
I'm not responsible for any issues or bugs you may encounter while using it.
'''

#Requires the sender package.
#pip install sender
from sender import Mail, Message

from subprocess import check_output
from datetime import datetime, timedelta

import os

#TODO: Change these depending on your PA webapp setup!

'''Email address settings'''
#The support email that the certificate update request goes to.
SUPPORT_EMAIL = "support@pythonanywhere.com"

#The name from which the email is coming (your name or your org's name)
FROM_NAME = "Person or Organization"

#The email address from which the request emails are being sent
FROM_EMAIL = "noreply@site.com"

#Dev email to CC and BCC when a certificate is updated
DEV_EMAIL = "developer@site.com"


'''PythonAnywhere user account and webapp settings'''
#Your pythonanywhere account username
PA_USERNAME = "PythonAnywhereUser"

#Your webapp's domain as configured in pythonanywhere 
WEBAPP_DOMAIN = "www.myPAwebapp.com"

'''Transactional email service settings'''
MAIL_SMTP_ADDRESS = 'smtp.mandrillapp.com'
MAIL_PORT = 587
MAIL_PASSWORD = 'Wow$uchSecur3'

def send_message(subject, to, body):
	mail = Mail(MAIL_SMTP_ADDRESS, port=MAIL_PORT,
	username=FROM_EMAIL, password=MAIL_PASSWORD,
			use_tls=False, use_ssl=False, debug_level=None)

	msg = Message()
	msg = Message(subject)
	msg.fromaddr = (FROM_NAME, FROM_EMAIL)
	msg.to = to

	msg.bcc = [DEV_EMAIL]
	msg.html = body

	mail.send(msg)
	return True

#Check the current date (renew every 60 days) to see if we need to renew
os.chdir('letsencrypt')

res = check_output(['bash', 'check.sh']).strip()
res = res.split("notAfter=")

#Format the date properly so we can tell when the certificate is set to expire.
datetime_object = datetime.strptime(res[1], '%b %d %H:%M:%S %Y %Z')
td = timedelta(days=29)
delta = datetime_object - td

if datetime.now() >= delta:
	print "SSL certificate has less than 1 month remaining, renewing!"

	#The path to your webapp's certificate file, built using the domain and your username.
	PA_APP_PATH = "/home/" + PA_USERNAME + "/letsencrypt/" + WEBAPP_DOMAIN
	
	#Call the letsencrypt  renewal script
	renew_result = check_output(['bash', 'renew.sh'])
	renew_result.replace('\n', '<br>')

	#Email the reminder, CC devs
	#Build the message body
	body = ""
	body += "TO: " + SUPPORT_EMAIL
	body +=	"Hi. I've renewed an SSL certificate for my account. I would like it to be installed.<br><br>"
	body += "username: " + PA_USERNAME + "<br>"
	body += "directory path: " + PA_APP_PATH + "<br>"
	body += "domain name: " WEBAPP_DOMAIN + "<br>"
	body += "<br>Thanks!"

	#Send first message to PA staff requesting updated renewal, BCC devs
	send_message("SSL Cert Renewal", SUPPORT_EMAIL, body)

	body = "The SSL certificate for" + WEBAPP_DOMAIN + "has been renewed. It was set to expire on " 
	body += res[1] + ".<br><br>The result of the renewal operations is attached below.<br><br>" 
	body += str(renew_result)

	#Send second message to devs detailing technical renewal details
	send_message("SSL Cert Renewal", DEV_EMAIL, body)

	print "Cert renewed & mail sent!"

else:
	print "Cert is not yet close to expiration, no action taken."
