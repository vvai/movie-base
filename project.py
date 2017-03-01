"""Server module."""
from flask import redirect, jsonify, url_for, flash
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Movie, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open("client_secrets.json", "r")
                       .read())["web"]["client_id"]
app = Flask(__name__)

engine = create_engine('sqlite:///moviebase.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def index():
    """Main page route."""
    genres = session.query(Genre).all()
    movies = session.query(Movie).order_by(Movie.id.desc()).limit(10)
    return render_template('index.html',
                           genres=genres,
                           movies=movies,
                           user=login_session)


@app.route('/login')
def login():
    """Login route."""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, user=login_session)


@app.route('/genre/<int:genre_id>/')
def showGenre(genre_id):
    """Show genre page."""
    genres = session.query(Genre).all()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movies = session.query(Movie).filter_by(
        genre_id=genre_id).all()
    return render_template('genre.html',
                           genres=genres,
                           movies=movies,
                           genre=genre,
                           user=login_session)


@app.route('/genre/<int:genre_id>/movie/<int:movie_id>')
def movie(genre_id, movie_id):
    """Show movie page."""
    movie = session.query(Movie).filter_by(id=movie_id).one()
    return render_template('movie.html',
                           movie=movie,
                           user=login_session)


@app.route('/genre/movie/new/', methods=['GET', 'POST'])
def newMovie():
    """New movie page and form handler."""
    if request.method == 'POST':
        if 'username' not in login_session:
            return redirect(url_for('login'))
        genre_id = request.form['genre_id']
        newMovie = Movie(title=request.form['title'],
                         description=request.form['description'],
                         year=request.form['year'],
                         director=request.form['director'],
                         genre_id=genre_id,
                         user_id=login_session.get('id'))
        session.add(newMovie)
        session.commit()
        flash("Movie '%s' created" % newMovie.title)
        return redirect(url_for('showGenre', genre_id=genre_id))
    else:
        genres = session.query(Genre).all()
        return render_template('add-movie.html',
                               genres=genres,
                               user=login_session)


@app.route('/genre/<int:genre_id>/movie/<int:movie_id>/edit',
           methods=['GET', 'POST'])
def editMovie(genre_id, movie_id):
    """Edit movie page and form handler."""
    editedMovie = session.query(Movie).filter_by(id=movie_id).one()
    if request.method == 'POST':
        if editedMovie.user_id != login_session.get('id'):
            return redirect(url_for('index'))
        if request.form['title']:
            editedMovie.title = request.form['title']
        if request.form['description']:
            editedMovie.description = request.form['description']
        if request.form['year']:
            editedMovie.year = request.form['year']
        if request.form['director']:
            editedMovie.director = request.form['director']
        if request.form['genre_id']:
            editedMovie.genre_id = request.form['genre_id']
        session.add(editedMovie)
        session.commit()
        flash("Movie '%s' was updated" % editedMovie.title)
        return redirect(url_for('showGenre',
                                genre_id=request.form['genre_id']))
    else:
        genres = session.query(Genre).all()
        return render_template(
            'edit-movie.html',
            genres=genres,
            genre_id=genre_id,
            movie_id=movie_id,
            movie=editedMovie,
            user=login_session)


@app.route('/genre/<int:genre_id>/movie/<int:movie_id>/delete',
           methods=['GET', 'POST'])
def deleteMovie(genre_id, movie_id):
    """Delete movie page and form handler."""
    movieToDelete = session.query(Movie).filter_by(id=movie_id).one()
    if request.method == 'POST':
        if movieToDelete.user_id != login_session.get('id'):
            return redirect(url_for('index'))
        session.delete(movieToDelete)
        session.commit()
        flash("Movie '%s' was deleted" % movieToDelete.title)
        return redirect(url_for('showGenre', genre_id=genre_id))
    else:
        return render_template('delete-movie.html',
                               movie=movieToDelete,
                               user=login_session)


@app.route('/genre/<int:genre_id>/movie/JSON')
def genreMoviesJSON(genre_id):
    """Get genre movies JSON."""
    # genre = session.query(Genre).filter_by(id=genre_id).one()
    movies = session.query(Movie).filter_by(
        genre_id=genre_id).all()
    return jsonify(movies=[m.serialize for m in movies])


@app.route('/genre/<int:genre_id>/movie/<int:movie_id>/JSON')
def movieJSON(genre_id, movie_id):
    """Get movie JSON."""
    movie = session.query(Movie).filter_by(id=movie_id).one()
    return jsonify(movie=movie.serialize)


@app.route('/genre/JSON')
def genresJSON():
    """Get all genres JSON."""
    genres = session.query(Genre).all()
    return jsonify(genres=[g.serialize for g in genres])


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Google auth route."""
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={0}'
           .format(access_token))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    print('check acess tocken:' + url)
    print(result)
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['google_id'] = data['id']
    # login_session['email'] = data['email']
    print('getUser')
    user = session.query(User).filter_by(google_id=data['id']).one()
    print(user)
    if not user:
        print('newUser')
        newUser = User(name=data['name'],
                       google_id=data['id'])
        session.add(newUser)
        session.commit()
        login_session['id'] = newUser.id
        # login_session['user'] = newUser
    else:
        print('justUser')
        login_session['id'] = user.id
        # login_session['user'] = user

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '  # NOQA
    flash("you are now logged in as {0}".format(login_session['username']))
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Disconnect google."""
    access_token = login_session.get('access_token')
    print('In gdisconnect access token is {0}'.format(access_token))
    print('User name is: ')
    print(login_session['username'])
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token={0}'.format(
        access_token)
    print('Url is:'+url)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    # if result['status'] == '200':
    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    # del login_session['email']
    del login_session['picture']
    # response = make_response(json.dumps('Successfully disconnected.'), 200)
    # response.headers['Content-Type'] = 'application/json'
    # return response
    return redirect(url_for('index'))
    # else:
    #     response = make_response(
    #         json.dumps('Failed to revoke token for given user.'), 400)
    #     response.headers['Content-Type'] = 'application/json'
    #     return response


if __name__ == '__main__':
    app.secret_key = 'some_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
