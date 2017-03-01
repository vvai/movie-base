# Movie base

## Description
This project represents CRUD web application. It contains movie ganres and movies.

## Configuration Instruction

This project uses `python3` programming language, `sqlalchemy flask oauth2client requests` python modules and `sqlite` database

## How to setup environment?

1. Install Python 3.X

2. Install python packages:

  `pip install sqlalchemy flask oauth2client requests`

3. run script which creates database:

  `python database_setup.py`

4. run script which populate database:

  `python add_items_to_db.py`

5. run flask server:

  `python project.py`

4. Open in browser `http://localhost:5000/`

You should be able to see web application.

## Operating Instructions

* [/](localhost:5000) - root endpoint
* [/genre/JSON](localhost:5000/genre/JSON) - get all genres as JSON
* [/genre/<int:genre_id>/movie/<int:movie_id>/JSON](localhost:5000/genre/<int:genre_id>/movie/<int:movie_id>/JSON) - get movie as JSON
* [/genre/<int:genre_id>/movie/JSON](localhost:5000/genre/<int:genre_id>/movie/JSON) - get all movies of ganre as JSON
* [/genre/<int:genre_id>/](localhost:5000/genre/<int:genre_id>/) - get all movies of genre
* [/genre/<int:genre_id>/movie/<int:movie_id>](localhost:5000/genre/<int:genre_id>/movie/<int:movie_id>) - get movie information
* [/genre/movie/new/](localhost:5000/genre/movie/new/) - create new movie page
* [/genre/<int:genre_id>/movie/<int:movie_id>/edit](localhost:5000/genre/<int:genre_id>/movie/<int:movie_id>/edit) - edit movie page
* [/genre/<int:genre_id>/movie/<int:movie_id>/delete](localhost:5000/genre/<int:genre_id>/movie/<int:movie_id>/delete) - delete movie page
