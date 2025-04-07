# MovieHub

### Overview

This project is a full-featured movie rating platform powered by Django, allowing users to browse, search, and review movies and TV shows. It includes user profiles and authentication, ratings, detailed media pages, and an admin dashboard for managing content.

### Requirements

 - Python 3.10+
 - pip
 - TogetherAI API key

### Download

Download the source code using the ```git clone``` command:

```bash
$ git clone https://github.com/wedkarz02/movie_hub.git
```

Or use the *Download ZIP* option from the Github repository [page](https://github.com/wedkarz02/movie_hub.git).

### Quick Setup

Create a virtual environment:

```bash
$ python3 -m venv venv
```
You might need to install the ```venv``` package in order to do so.

Install required packages in the virtual environment from the ```requirements.txt``` file:

```bash
$ venv/bin/pip3 install -r requirements.txt
```

Run database migrations:

```bash
$ venv/bin/python3 manage.py migrate
```
```movie_hub``` uses sqlite3 which is included with Django, so there's no need to install it manually.

Create a super user account:

```bash
$ venv/bin/python3 manage.py createsuperuser
```

and fill in the required information.

### Usage

This application needs ```TOGETHER_API_KEY``` environment variable to work properly. You can obtain the API key by logging into your [TogetherAI](https://www.together.ai/) account and navigating to the dashboard. 

Once you have the API key, either run the application with the value:

```bash
$ TOGETHER_API_KEY=xxx venv/bin/python3 manage.py runserver
```

or export the ```TOGETHER_API_KEY``` in system configuration:

```bash
# ~/.bashrc
export TOGETHER_API_KEY=xxx
```

and start the server:

```bash
$ venv/bin/python3 manage.py runserver
```

With default configuration, the server is live on ```http://127.0.0.1:8000```.

Optionally you can populate the database with movies from the ```movies.json``` file:

```bash
$ venv/bin/python3 manage.py load_movies movies.json
```

If you'd like to change the default profile picture for new users, swap the ```media/default.jpg``` file for your image (needs to be named ```default.jpg``` and be located in ```media``` directory).

### License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/wedkarz02/movie_hub/blob/main/LICENSE) file for more info.
