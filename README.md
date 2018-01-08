# PA_SSL_AutoRenew
A Python script to automatically renew LetsEncrypt SSL certificates on PythonAnywhere.

If you're using LetsEncrypt for SSL certificates on PythonAnywhere webapps, you probably know that your certificate expires every 90 days. You probably also know that you can't configure an autorenewal since you need to email the PA staff and let them know you have a new certificate to be installed.

The script will check an SSL certificate for the domain of your choice to see if it's going to expire in 29 days or less. If it is, it will automatically run the LetsEncrypt renewal code and then email the PythonAnywhere support staff letting them know you have an updated certificate you'd like them to install.

# Installation and Setup
THIS WILL ONLY WORK IF YOU'VE ALREADY SET UP AND RUN LETSENCRYPT ONCE! If you haven't, follow [this](https://help.pythonanywhere.com/pages/LetsEncrypt/) to do so.


1. You'll need a transactional email service such as Mandrill or Mailgun in order to send emails. I'm using Mandrill. 
1. Make sure the Python Sender package is installed. If it isn't, use `pip install sender`.
1. Edit `renew.py`: Set all of the variables in lines 14-36, and copy to your PythonAnywhere home directory.
1. Edit `renew.sh`: Replace `YOUR_TLD_HERE` with your webapp's top-level domain and copy to the `letsencrypt/` directory.
1. Edit `check.sh`: Replace `YOUR_TLD_HERE` with your webapp's top-level domain and copy to the `letsencrypt/` directory.
 (You may need to `chmod +x` `renew.sh` and `check.sh` after you've copied them if you're having trouble.)
1. Make a PythonAnywhere scheduled task pointing to `renew.py`. Daily is fine; it will only renew and send the emails when the certificate is close to expiration.
