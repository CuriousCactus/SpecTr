#!/usr/bin/env python
#
import cgi
form = cgi.FieldStorage() # instantiate only once!
password = form.getfirst('password', 'empty')

# Avoid script injection escaping the user input
password = cgi.escape(password)

print "Content-Type: text/html"

correctpassword=open("password.txt", "r").read()

if password == correctpassword:
    print """\
    Content-Type: text/html\n
    <html><body>
    <p>Hello!</p>
    <img src="pulpit.jpg"/>
    </body></html>
    """

else:
    print """\
    Content-Type: text/html\n
    <html><body>
    <p>Wrong!</p>
    </body></html>
    """

