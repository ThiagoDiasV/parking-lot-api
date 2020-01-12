# Install Parking MK API Rest

You can run Parking MK API Rest using the Python of your operational system or using Docker. We strongly recommend the use of Docker to avoid environments issues.

## Clone this repository

In your root window, run this command to clone this repo

    git clone https://github.com/ThiagoDiasV/parking-mk-challenge.git

Now you can try the API using Python or Docker.

## Using Docker and docker compose

First you need to init a daemon with dockerd, so run dockerd:

    root $ dockerd

OR

    root $ sudo dockerd

Now, access the parking-mk-challenge directory:

root \$ cd parking-mk-challenge/

And then with Docker and docker-compose, run:

    parking-mk-challenge $ docker-compose up --build

This command above will:

- Create and migrate database
- Run unit tests
- Run server

Now you will be able to navigate through the Parking MK API.

After testing, to stop the created container:

    parking-mk-challenge $ docker-compose down

## Using local Python 3.8+

Prefer to create a Python virtual environment and then

    (venv) root $ cd parking-mk-challenge/
    (venv) parking-mk-challenge $ pip install -r requirements.txt

After installing requirements run:

    (venv) parking-mk-challenge $ python geomk/manage.py migrate
    (venv) parking-mk-challenge $ python geomk/manage.py runserver

Now you can try the API.

This API is covered by some automatized tests. You can run these tests using the command below:

    (venv) parking-mk-challenge $ python geomk/manage.py test api.tests

## Testing CI using CircleCI

This API and the Github repository are covered by CircleCI continuous integration tool.

To try locally, you'll need CircleCI CLI tool. Install this and run the command below

    parking-mk-challenge $ circlecli build
