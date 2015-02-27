#!/usr/bin/python
import re
import urllib2
from cookielib import CookieJar
import urllib

cas_username = "" # put your BYU Username Here
cas_password = "" # put your BYU password here

def send_email():
        import smtplib

        gmail_user = "from-email@gmail.com"
        gmail_pwd = "password"
        FROM = 'from-email@gmail.com'
        TO = ['notify_email@gmail.com'] #must be a list
        SUBJECT = "Application was Updated!"
        TEXT = "Hey!  I'm a bot that was programmed to check your application status.  It was updated in the last few minutes!  Go see what it says!   Also you'll need to disable the script or you'll keep getting spammed..."

        # Prepare actual message
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            #server = smtplib.SMTP(SERVER)
            server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            #server.quit()
            server.close()
            print 'successfully sent the mail'
        except:
            print "failed to send mail"


url_one = "https://cas.byu.edu/cas/login"
url_two = "https://y.byu.edu/ry/ae/prod/ces/cgi/admissionsStatus.cgi"
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

url = "https://cas.byu.edu/cas/login?service=https%3A%2F%2Fy.byu.edu%2Fvalidate%3Ftarget%3Dhttps%253A%252F%252Fy.byu.edu%252Fry%252Fae%252Fprod%252Fces%252Fcgi%252FadmissionsStatus.cgi"


response = opener.open(url_one)
content = response.read()

lte = re.search("name=\"lt\" value=\"(.*?)\"",content).group(1)
execution = re.search("name=\"execution\" value=\"(.*?)\"",content).group(1)
values = {"username":cas_username,"password":cas_password,"execution":execution,"lt":lte,"_eventId":"submit"}
data_encoded = urllib.urlencode(values)

response = opener.open(url_one,data_encoded)
content = response.read()

response = opener.open(url_two)
content = response.read()
content = content.splitlines()
num = 0
for line in content:
        num = num + 1
        if "<b>BYU</b>" in line:
                break
if "Complete" not in content[num+1]:
        send_email()
