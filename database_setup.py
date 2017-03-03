"""Module creates database."""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, MetaData

Base = declarative_base()


class User(Base):
    """Table for user information."""

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    google_id = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return serialized user object."""
        return {
            'id': self.id,
            'name': self.name,
            'google_id': self.google_id,
        }


class Genre(Base):
    """Class for movie genre."""

    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format."""
        return {
            'id': self.id,
            'name': self.name,
        }


class Movie(Base):
    """Class for movie."""

    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(500))
    year = Column(String(8))
    director = Column(String(250))
    genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship(Genre)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'year': self.year,
            'director': self.director,
        }


def connect(user, password, db, host='localhost', port=5432):
    """Return a connection and a metadata object."""
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    # The return value of create_engine() is our connection object
    con = create_engine(url, client_encoding='utf8')
    # We then bind the connection to MetaData()
    meta = MetaData(bind=con, reflect=True)
    return con, meta


# engine = create_engine('sqlite:///moviebase.db')
engine, meta = connect('postgres', '123', 'movies')


Base.metadata.create_all(engine)
