# flask_api_template

A template for implementing REST API microservices with Flask and Python.

I haven't decided how much front end code will be included here. One thing at a time.

Just to get a taste of where this project is going, see this blog posting
[Python microservices with Flask](https://blog.viktoradam.net/2017/12/16/python-microservices-with-flask/).

## Set up

For development I usually run in a conda environment on the local machine.
VSCODE is set up (see .vscode/launch.json) to launch hello_api.py for you on F5.

Command to set up and activate an environment:

```console
$ conda create --name=flask --file=requirements
$ conda activate flask
```

My use case is so microscopic that deployment and scaling are non-issues for me,
but normally I run the app in a Docker container using "waitress" as the server.

```console
$ docker-compose build
$ docker run --rm -ti -p 5000:5000 flask:latest
```

When you open a browser http://localhost:5000, you should see a Hello, World message.

## Test

I use [httpie from the command line](https://httpie.io/docs/cli/usage)
to test, httpie gets installed in the "flask" environment so be sure you activate it.

By default VSCode runs hello_rest.py which implements a simple list of strings.

```bash
    # POST items to the list
    http "http://localhost:5000/list" item="apple"
    http "http://localhost:5000/list" item="tanker truck"
    http "http://localhost:5000/list" item="brick"
    http "http://localhost:5000/list" item="water bottle"
    # GET the list
    http "http://localhost:5000/list"
    # DELETE an item
    http DELETE "http://localhost:5000/list" item="brick"
```

Creating the user database with SqlAlchemy did not apply UNIQUE constraint.

```console
$ sqlite3 users.db
sqlite> CREATE TABLE user(id INTEGER PRIMARY KEY, username VARCHAR UNIQUE, password VARCHAR, role VARCHAR);
sqlite> .schema user
sqlite> .quit
```

## Fork

I need to look at the official way to use templates, I think I can create 
a new project repository using
this one as a template, so I don't actually have to fork it.
## Resources

I started from my older project, [flask_template](https://github.com/Wildsong/flask_template).

I started with [Python Flask Web Development](https://www.amazon.com/Flask-Web-Development-Developing-Applications-dp-1491991739/dp/1491991739/ref=dp_ob_title_bk) but I don't have access to it right now. I wonder what Mr. Grinberg's **Flask Mega-Tutorial** is like. It's available as a book
or as this blog. [The Flask Mega-Tutorial Part I: Hello, World!](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

The book "Building REST APIs with Flask: Create Python Web Services with MySQL"
promised REST but just delivered an app.

I own a copy of [Mastering Flask Web Development]() and chapter 8 is "Building RESTful APIs".

Chapter 11 "Web API with Flask" from [Building Web Apps with Python and Flask](https://acm.percipio.com/books/3ae6d909-d674-4aa7-a86d-2f52c68faddf#epubcfi(/6/4!/4/2[epubmain]/2[g8f0e2f46-2107-41a5-ad51-53de91d9b63f]/2/2/1:0))

I should look at [Designing Microservices with Django](https://acm.percipio.com/books/1ab062c7-a577-4e14-b8f4-a48778af7142#epubcfi(/6/4!/4/2[epubmain]/2[g720486a1-56bf-484b-809d-4dfcfca35f1d]/2/2/1:0)) but Django always seems like such a heavy lift for a starting point.

