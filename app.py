#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import datetime
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy import exc
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database

db.init_app(app)
migrate = Migrate(app,db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(500), default='')
    seeking_talent = db.Column(db.Boolean, default=False)
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    shows = db.relationship('Show', backref='Venue', lazy='dynamic')
    
    def __init__(self, name, genres, address, city, state, phone, website, facebook_link, image_link,
                 seeking_description,seeking_talent=False):
        self.name = name
        self.genres = genres
        self.city = city
        self.state = state
        self.address = address
        self.phone = phone
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.website = website
        self.seeking_talent = seeking_talent
        self.seeking_description = seeking_description
        
    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'


    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    city = db.Column(db.String(500))
    state = db.Column(db.String(500))
    phone = db.Column(db.String(500))
    genres = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500), default=' ')
    website = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Artist', lazy=True)
    
    
    def __init__(self, name, genres, city, state, phone, image_link, website, facebook_link,
                 seeking_venue=False, seeking_description=""):
        self.name = name
        self.genres = genres
        self.city = city
        self.state = state
        self.phone = phone
        self.website = website
        self.facebook_link = facebook_link
        self.seeking_venue = seeking_venue
        self.seeking_description = seeking_description
        self.image_link = image_link
    
    
    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'
        
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Show'
    
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    
    
    def __init__(self, venue_id,artist_id,start_time):
        self.venue_id = venue_id
        self.artist_id = artist_id
        self.start_time = start_time

    
def __repr__(self):
        return f'<Show {self.id} {self.time} {self.artist_id} {self.venue_id}>'
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    areas = db.session.query(Venue.city, Venue.state).distinct(Venue.city, Venue.state)
    data = []
    for area in areas:
        venues = db.session.query(Venue).filter(Venue.city==area.city).filter(Venue.state==Venue.state)
        data.append({
            'city': area.city,
            'state': area.state,
            'venue':[]
            })
        for venue in venues:
            num_upcoming_shows = len(venue.shows.filter(Show.time > datetime.now()))
            data['venue'].append({
                'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': num_upcoming_shows
                })
        
        
    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  venues = db.session.query(Venue)
  result = []
  for venue in venues:
      if search_term in venue.name:
          result.append(venue)
  count = len(result)
  response = {
        "count": count,
        "data": result
    }
  return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.filter(Venue.id == venue_id).first()
  past = db.session.query(Show).filter(Show.venue_id == venue_id).filter(
        Show.start_time < datetime.now()).join(Artist, Show.artist_id == Artist.id).add_columns(Artist.id, Artist.name,
                                                                                                Artist.image_link,
                                                                                                Show.start_time).all()

  upcoming = db.session.query(Show).filter(Show.venue_id == venue_id).filter(
        Show.start_time > datetime.now()).join(Artist, Show.artist_id == Artist.id).add_columns(Artist.id, Artist.name,
                                                                                                Artist.image_link,
                                                                                                Show.start_time).all()
  past_shows = []
  upcoming_shows = []
  
  for i in upcoming:
        upcoming_shows.append({
            'artist_id': i[1],
            'artist_name': i[2],
            'image_link': i[3],
            'start_time': str(i[4])
        })

  for i in past:
        past_shows.append({
            'artist_id': i[1],
            'artist_name': i[2],
            'image_link': i[3],
            'start_time': str(i[4])
        })
        
  if venue is None:
      abort(404)
      
  data = {
      'id': venue_id,
      'genres': venue.genre,
      'city': venue.city,
      'state': venue.state,
      'address': venue.address,
      'phone': venue.phone,
      'website': venue.website,
      'facebook_link': venue.facebook_link,
      'seeking_talent': venue.seeking_talent,
      'seeking_description': venue.seeking_description,
      'upcoming_shows_count': len(upcoming_shows),
      'past_show_count':len(past_shows),
      'upcoming_shows': upcoming_shows,
      'past_shows': past_shows
      }

  return render_template('pages/show_venue.html', venue=data)

  


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  venue = Venue(
            name=request.form['name'],
            city=request.form['city'],
            state=request.form['state'],
            address=request.form['address'],
            phone=request.form['phone'],
            genres=request.form.getlist('genres'),
            image_link=request.form['image_link'],
            facebook_link=request.form['facebook_link'],
            website=request.form['website_link'],
            seeking_talent= True if request.form['seeking_talent'] == 'y' else False,
            seeking_description=request.form['seeking_description']
        )
  db.session.add(venue)
  try:
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully added!')
  except exc.SQLAlchemyError as e:
        print(e)
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be added')
        db.session.rollback()
  finally:
        db.session.close()
  return render_template('pages/home.html')

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
      Venue.query.filter(Venue.id == venue_id).delete()
      db.session.commit()
  except:
      db.session.rollback()
  finally:
      db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  artists = []
  for a in db.session.query(Artist):
      if a.name in search_term:
          artists.append(a)
  count = len(artists)
  result = {
        "count": count,
        "data": artists
    }
  return render_template('pages/search_artists.html', results=result, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.filter(Artist.id == artist_id).first()
  if artist == None:
      abort(404)
  shows = artist.shows
  past_shows = []
  upcoming_shows =[]
  for show in shows:
      if show.time < datetime.now():
          past_shows.append(show)
      elif show.time > datetime.now():
          upcoming_shows.append(show)
  data = {
      'id': artist_id,
      'genres': artist.genre,
      'city': artist.city,
      'state': artist.state,
      'address': artist.address,
      'phone': artist.phone,
      'website': artist.website,
      'facebook_link': artist.facebook_link,
      'seeking_talent': artist.seeking_talent,
      'seeking_description': artist.seeking_description,
      'upcoming_shows_count': len(upcoming_shows),
      'past_show_count':len(past_shows),
      'upcoming_shows': upcoming_shows,
      'past_shows': past_shows
      }
  return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter(Artist.id == artist_id).fisrt()
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    new_artist = Artist(
      name=request.form['name'],
      genres=request.form['genres'],
      city=request.form['city'],
      state= request.form['state'],
      phone=request.form['phone'],
      website=request.form['website_link'],
      image_link=request.form['image_link'],
      facebook_link=request.form['facebook_link'],
      seeking_venue= True if request.form['seeking_venue'] == 'y' else False,
      seeking_description=request.form['seeking_description']
   )
    
    db.session.add(new_artist)
    try:
        db.session.commit()
        flah('Artist' + request.form['name'] + 'was successfully listed!')
    except exc.SQLAlchemyError as e:
        print(e)
        flash('An error ocurred. Artist' + request.form['name'] + 'could not be listed.')
    return redirect(url_for('show_artist', artist_id=artist_id))
    


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter(Venue.id == venue_id).first()
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  new_venue = Venue(
      name=request.form['name'],
      genres=request.form.getlist('genres'),
      address=request.form['address'],
      city=request.form['city'],
      state=request.form['state'],
      phone=request.form['phone'],
      website=request.form['website'],
      facebook_link=request.form['facebook_link'],
      image_link=request.form['image_link'],
      seeking_talent=True if request.form['seeking_talent'] == 'y' else False,
      seeking_description=request.form['seeking_description']
    )
    #insert new venue records into the db
  db.session.add(new_venue)
  try:
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except exc.SQLAlchemyError:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
      
  new_artist = Artist(
      name=request.form['name'],
      genres=request.form['genres'],
      city=request.form['city'],
      state= request.form['state'],
      phone=request.form['phone'],
      website=request.form['website_link'],
      image_link=request.form['image_link'],
      facebook_link=request.form['facebook_link'],
      seeking_venue= True if request.form['seeking_venue'] == 'y' else False,
      seeking_description=request.form['seeking_description']
    )
    
    # on successful db insert, flash success
  db.session.add(new_artist)
  try:
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except exc.SQLAlchemyError as e:
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
      print(e)
      flash('An error occurred. Artist ' + request.form['name'] + 'could not be listed. ')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
    data = Show.query.join(Artist, Artist.id == Show.artist_id).join(Venue, Venue.id == Show.venue_id).all()

    response = []
    for show in data:
        response.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": str(show.start_time)
        })
    return render_template('pages/shows.html', shows=response)

  

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  new_show = Show(
      venue_id=request.form['venue_id'],
      artist_id=request.form['artist_id'],
      start_time=request.form['start_time'],
    )
  db.session.add(new_show)
  try:
        db.session.commit()

    # on successful db insert, flash success
        flash('Show was successfully listed!')
  except exc.SQLAlchemyError:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occured. Show could not be listed.')
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
