Nathan Lapinski and Louis Francois 1/30/2014

This README accompanies a simple REST API built using Flask and Python. It allows the creation of users, and groups that contain users.
Build instructions, as well as some details regarding the implementation, are included in here.

-Build Instructions-
These instructions assume that you are working on a Linux machine. Alternatively, all that you really need to run this API is Flask and curl.

1) mkdir rest-api
2) cd rest-api
3) virtualenv flask                 #create a virtual env
4) flask/bin/pip install flask       #and install the Flask microframework

From here, place the dev_app.py file in the current directory (rest-api) and set its permissions accordingly

5) chmod a+x dev_app.py

That's pretty much it. Now we simply run it from the command line like so:
6) ./dev_app.py

I'm very security conscious when I write any software, so I thought it would be wise to include some simple authentication using HTTPauth
7) flask/bin/pip install flask-httpauth

The only effect this has is that every curl command that we issue to interact with the api must include the credentials:
-u planet:python

The server should be up and running at this point. From here, I like to open a second terminal and interact with the api using the curl utility. If 
you don't have curl installed, you can download it here: http://curl.haxx.se/download.html

From here, some simple unit tests that can be run to verify correctness of the API are as follows.

Ok, on to unit tests.

-Unit Tests-
#1 Get a list of current users
curl -u planet:python -i http://localhost:5000/users/

will return the default, sample user records included with the app

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 179
Server: Werkzeug/0.9.6 Python/2.6.5
Date: Tue, 30 Dec 2014 09:58:24 GMT

{
  "records": [
    {
      "first_name": "Joe", 
      "groups": [
        "admins", 
        "users"
      ], 
      "last_name": "Smith", 
      "userid": "jsmith"
    }
  ]
}

#2 Post a new user
curl -u planet:python -i -H "Content-Type: application/json" -X POST -d '{"first_name":"Albert","last_name":"Einstein","userid":"ale","groups":["test_group"]}' http://localhost:5000/users/ale

This creates a user record, and places him in the default group "test_group". If a user record is POSTed that references a group that doesn't exist - it generates a 404 error.

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 143
Server: Werkzeug/0.9.6 Python/2.6.5
Date: Tue, 30 Dec 2014 10:00:37 GMT

{
  "record": {
    "first_name": "Albert", 
    "groups": [
      "test_group"
    ], 
    "last_name": "Einstein", 
    "userid": "ale"
  }
}

#3 Get the user record with userid ale
curl -u planet:python -i http://localhost:5000/users/ale

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 143
Server: Werkzeug/0.9.6 Python/2.6.5
Date: Tue, 30 Dec 2014 10:02:48 GMT

{
  "record": {
    "first_name": "Albert", 
    "groups": [
      "test_group"
    ], 
    "last_name": "Einstein", 
    "userid": "ale"
  }
}

#4 Suppoese Albert wants to change his name to Al
curl -u planet:python -i -H "Content-Type: application/json" -X PUT -d '{"first_name":"Al","last_name":"Einstein","userid":"ale","groups":["test_group"]}' http://localhost:5000/users/ale

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 139
Server: Werkzeug/0.9.6 Python/2.6.5
Date: Tue, 30 Dec 2014 10:04:14 GMT

{
  "record": {
    "first_name": "Al", 
    "groups": [
      "test_group"
    ], 
    "last_name": "Einstein", 
    "userid": "ale"
  }
}

#5 Ok, let's create an empty group, called genius
curl -u planet:python -i -H "Content-Type: application/json" -X POST -d '{"group_name":"genius"}' http://localhost:5000/groups/genius

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 68
Server: Werkzeug/0.9.6 Python/2.6.5
Date: Tue, 30 Dec 2014 10:06:23 GMT

{
  "record": {
    "group_name": "genius", 
    "members": []
  }
}

#6 We should probably add Al to that group, so let's PUT a new member list
curl -u  planet:python -i -H "Content-Type: application/jso" -X PUT -d '{"group_name":"genius","members":["ale"]}' http://localhost:5000/groups/genius

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 85
Server: Werkzeug/0.9.6 Python/2.6.5
Date: Tue, 30 Dec 2014 10:08:17 GMT

{
  "record": {
    "group_name": "genius", 
    "members": [
      "ale"
    ]
  }
}

#7 Let's maje sure that updated in Al's user record as well
curl -uplanet:python -i http://localhost:5000/users/aleHTTP/1.0 200 OK

Content-Type: application/json
Content-Length: 156
Server: Werkzeug/0.9.6 Python/2.6.5
Date: Tue, 30 Dec 2014 10:09:01 GMT

{
  "record": {
    "first_name": "Al", 
    "groups": [
      "test_group", 
      "genius"
    ], 
    "last_name": "Einstein", 
    "userid": "ale"
  }
}

Yep!

#8 Okay, now, let's DELETE the genius group
curl -u planet:python -i -X DELETE http://localhost:5000/groups/genius

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 20
Server: Werkzeug/0.9.6 Python/2.6.5
Date: Tue, 30 Dec 2014 10:10:41 GMT

and it updated automatically in Albert's user record as well - he is no longer a member of the group genius, since it no longer exists.

curl -u planet:python -ihttp://localhost:5000/users/aleHTTP/1.0 200 OK

Content-Type: application/json
Content-Length: 139
Server: Werkzeug/0.9.6 Python/2.6.5
Date: Tue, 30 Dec 2014 10:11:03 GMT

{
  "record": {
    "first_name": "Al", 
    "groups": [
      "test_group"
    ], 
    "last_name": "Einstein", 
    "userid": "ale"
  }
}

There are plenty of other unit tests that I ran, such as verifying that posting to an existing user gives a 409 conflict error, PUT'ing to a non-existent record 
generates a 404 error, etc. 