"""Add sample data to db."""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Movie, Genre, User


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
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Add user
user1 = User(google_id="115897189862705908491", name="Vitalik Vojtehovsky")
session.add(user1)
session.commit()
user_id = user1.id

# Add some genres
genre1 = Genre(name="Horror", user_id=user_id)
session.add(genre1)
session.commit()

movie1 = Movie(
    title="The Shining",
    description="Frustrated writer Jack Torrance takes a job as the winter caretaker at the ominous, mountain-locked Overlook Hotel so that he can write in peace. When he arrives there with his wife and son, they learn that the previous caretaker had gone mad. Slowly Jack becomes possessed by the evil, demonic presence in the hotel.",  # NOQA
    year="1980",
    director="Stanley Kubrick",
    genre=genre1,
    user_id=user_id
    )
session.add(movie1)
session.commit()

movie2 = Movie(
    title="The Thing",
    description="The stage is set for havoc and terror when a 12-man research team finds an alien being that has fallen from the sky and has been buried for over 100,000 years.",  # NOQA
    year="1982",
    director="John Carpenter",
    genre=genre1,
    user_id=user_id
    )
session.add(movie2)
session.commit()

movie3 = Movie(
    title="The Texas Chain Saw Massacre",
    description="A group of teenagers on the road in Texas stop off at the wrong farm and encounter a family gone awry. Once abattoir workers, the decay of the Southern rural economy has left them unemployed, and the directionless father and sons take to using their butchering skills on passing people. One by one, the kids encounter members of the grisly family.",  # NOQA
    year="1974",
    director="Tobe Hooper",
    genre=genre1,
    user_id=user_id
    )
session.add(movie3)
session.commit()

movie4 = Movie(
    title="The Others",
    description="The Others is a 2001 Spanish-American supernatural gothic horror film with elements of psychological horror. It was written, directed, and scored by Alejandro Amenábar. It stars Nicole Kidman and Fionnula Flanagan.",  # NOQA
    year="2001",
    director="Alejandro Amenábar",
    genre=genre1,
    user_id=user_id
    )
session.add(movie4)
session.commit()


genre2 = Genre(name="Thriller", user_id=user_id)
session.add(genre2)
session.commit()

movie5 = Movie(
    title="The Silence of the Lambs",
    description="A psychopath nicknamed Buffalo Bill is murdering women across the Midwest. Believing it takes one to know one, the FBI sends Agent Clarice Starling to interview a demented prisoner who may provide clues to the killer's actions. That prisoner is psychiatrist Dr. Hannibal Lecter, a brilliant, diabolical cannibal who agrees to help Starling only if she'll feed his morbid curiosity with details of her own complicated life.",  # NOQA
    year="1991",
    director="Jonathan Demme",
    genre=genre2,
    user_id=user_id
    )
session.add(movie5)
session.commit()

movie6 = Movie(
    title="The Sixth Sense",
    description="Young Cole Sear (Haley Joel Osment) is haunted by a dark secret: he is visited by ghosts. Cole is frightened by visitations from those with unresolved problems who appear from the shadows. He is too afraid to tell anyone about his anguish, except child psychologist Dr. Malcolm Crowe (Bruce Willis). As Dr. Crowe tries to uncover the truth about Cole's supernatural abilities, the consequences for client and therapist are a jolt that awakens them both to something unexplainable.",  # NOQA
    year="1999",
    director="M. Night Shyamalan",
    genre=genre2,
    user_id=user_id
    )
session.add(movie6)
session.commit()

movie7 = Movie(
    title="The Machinist",
    description="The Machinist is a 2004 psychological thriller film directed by Brad Anderson and written by Scott Kosar. The film stars Christian Bale and features Jennifer Jason Leigh, John Sharian, Aitana Sánchez-Gijón, and Michael Ironside in supporting roles.",  # NOQA
    year="2004",
    director="Brad Anderson",
    genre=genre2,
    user_id=user_id
    )
session.add(movie7)
session.commit()

movie8 = Movie(
    title="Mulholland Drive",
    description="Along Mulholland Drive nothing is what it seems. In the unreal universe of Los Angeles, the city bares its schizophrenic nature, an uneasy blend of innocence and corruption, love and loneliness, beauty and depravity. A woman is left with amnesia following a car accident. An aspiring young actress finds her staying in her aunt's home. The puzzle begins to unfold, propelling us through a mysterious labyrith of sensual experiences until we arrive at the intersection of dreams and nightmares.",  # NOQA
    year="2001",
    director="David Lynch",
    genre=genre2,
    user_id=user_id
    )
session.add(movie8)
session.commit()

genre3 = Genre(name="Documentary film", user_id=user_id)
session.add(genre3)
session.commit()

movie9 = Movie(
    title="Man on Wire",
    description="Man on Wire is a 2008 British biographical documentary film directed by James Marsh. The film chronicles Philippe Petit's 1974 high-wire walk between the Twin Towers of New York's World Trade Center.",  # NOQA
    year="2008",
    director="James Marsh",
    genre=genre3,
    user_id=user_id
    )
session.add(movie9)
session.commit()

movie10 = Movie(
    title="The Thin Blue Line",
    description="The Thin Blue Line is a 1988 American documentary film by Errol Morris, depicting the story of Randall Dale Adams, a man convicted and sentenced to death for a murder he did not commit.",  # NOQA
    year="1988",
    director="Errol Morris",
    genre=genre3,
    user_id=user_id
    )
session.add(movie10)
session.commit()

movie11 = Movie(
    title="Citizenfour",
    description="Citizenfour is a 2014 documentary film directed by Laura Poitras, concerning Edward Snowden and the NSA spying scandal.",  # NOQA
    year="2014",
    director="Laura Poitras",
    genre=genre3,
    user_id=user_id
    )
session.add(movie11)
session.commit()

movie12 = Movie(
    title="The Look of Silence",
    description="The Look of Silence is a 2014 internationally co-produced documentary film directed by Joshua Oppenheimer about the Indonesian killings of 1965–66. The film is a companion piece to Oppenheimer's 2012 documentary The Act of Killing.",  # NOQA
    year="2014",
    director="Joshua Oppenheimer",
    genre=genre3,
    user_id=user_id
    )
session.add(movie12)
session.commit()

genre4 = Genre(name="Drama", user_id=user_id)
session.add(genre4)
session.commit()

movie13 = Movie(
    title="American Beauty",
    description="American Beauty is a 1999 American drama film directed by Sam Mendes and written by Alan Ball. Kevin Spacey stars as Lester Burnham, a 42-year-old advertising executive who has a midlife crisis when he ...",  # NOQA
    year="19999",
    director="Sam Mendes",
    genre=genre4,
    user_id=user_id
    )
session.add(movie13)
session.commit()

movie14 = Movie(
    title="The Shawshank Redemption",
    description="In 1946, a banker named Andy Dufresne (Tim Robbins) is convicted of a double murder, even though he stubbornly proclaims his innocence. He's sentenced to a life term at the Shawshank State Prison in Maine, where another lifer, Ellis Red Redding (Morgan Freeman), picks him as the new recruit most likely to crack under the pressure.",  # NOQA
    year="1994",
    director="Frank Darabont",
    genre=genre4,
    user_id=user_id
    )
session.add(movie14)
session.commit()

movie15 = Movie(
    title="Requiem for a Dream",
    description="Requiem for a Dream is a 2000 American psychological drama film directed by Darren Aronofsky and starring Ellen Burstyn, Jared Leto, Jennifer Connelly, and Marlon Wayans.",  # NOQA
    year="2000",
    director="Darren Aronofsky",
    genre=genre4,
    user_id=user_id
    )
session.add(movie15)
session.commit()

movie16 = Movie(
    title="Rocky",
    description="A slightly dimwitted amateur boxer from Philadelphia's tough neighborhood gets a surprise shot at fighting for the heavyweight championship, while at the same time he finds love in the arms of a shy, reclusive girl who works in the local pet store.",  # NOQA
    year="1976",
    director="John G. Avildsen",
    genre=genre4,
    user_id=user_id
    )
session.add(movie16)
session.commit()

genre5 = Genre(name="Animation", user_id=user_id)
session.add(genre5)
session.commit()

movie17 = Movie(
    title="Zootopia",
    description="The modern mammal metropolis of Zootopia is a city like no other. Comprised of habitat neighborhoods like ritzy Sahara Square and frigid Tundratown, it's a melting pot where animals from every environment live together - a place where no matter what you are, from the biggest elephant to the smallest shrew, you can be anything. But when rookie Officer Judy Hopps arrives, she discovers that being the first bunny on a police force of big, tough animals isn't so easy.",  # NOQA
    year="2016",
    director="Byron Howard, Rich Moore",
    genre=genre5,
    user_id=user_id
    )
session.add(movie17)
session.commit()

movie18 = Movie(
    title="Finding Nemo",
    description="Finding Nemo is a 2003 American computer-animated comedy-drama adventure film produced by Pixar Animation Studios and released by Walt Disney Pictures.",  # NOQA
    year="2003",
    director="Andrew Stanton, Lee Unkrich",
    genre=genre5,
    user_id=user_id
    )
session.add(movie18)
session.commit()

movie19 = Movie(
    title="Shrek",
    description="Once upon a time, in a far away swamp, there lived an ornery ogre named Shrek whose precious solitude is suddenly shattered by an invasion of annoying fairy tale characters. There are blind mice in his food, a big, bad wolf in his bed, three little homeless pigs and more, all banished from their kingdom by the evil Lord Farquaad. Determined to save their home--not to mention his own--Shrek cuts a deal with Farquaad and sets out to rescue the beautiful Princess Fiona to be Farquaad's bride.",  # NOQA
    year="2001",
    director="Vicky Jenson, Andrew Adamson",
    genre=genre5,
    user_id=user_id
    )
session.add(movie19)
session.commit()

movie20 = Movie(
    title="WALL-E",
    description="WALL-E, short for Waste Allocation Load Lifter Earth-class, is the last robot left on Earth. He spends his days tidying up the planet, one piece of garbage at a time. But during 700 years, WALL-E has developed a personality, and he's more than a little lonely. Then he spots EVE (Elissa Knight), a sleek and shapely probe sent back to Earth on a scanning mission. Smitten WALL-E embarks on his greatest adventure yet when he follows EVE across the galaxy.",  # NOQA
    year="2008",
    director="Andrew Stanton",
    genre=genre5,
    user_id=user_id
    )
session.add(movie20)
session.commit()

genre6 = Genre(name="Comedy", user_id=user_id)
session.add(genre6)
session.commit()

movie21 = Movie(
    title="Borat: Cultural Learnings of America for Make Benefit Glorious Nation of Kazakhstan",  # NOQA
    description="Borat! Cultural Learnings of America for Make Benefit Glorious Nation of Kazakhstan is a 2006 British-American mockumentary comedy film.",  # NOQA
    year="2006",
    director="Larry Charles",
    genre=genre6,
    user_id=user_id
    )
session.add(movie21)
session.commit()

movie22 = Movie(
    title="American Pie",
    description="American Pie is a 1999 teen sex comedy film written by Adam Herz and directed by brothers Paul and Chris Weitz, in their directorial film debut. It is the first film in the American Pie theatrical series.",  # NOQA
    year="1999",
    director="Paul Weitz, Chris Weitz",
    genre=genre6,
    user_id=user_id
    )
session.add(movie22)
session.commit()

movie23 = Movie(
    title="The Big Lebowski",
    description="The Coen brothers and their agreeable cast make more fun than sense with this scattered farce about a pothead bowler who is mistaken for a deadbeat philanthropist and drawn into a cluster of kidnapers, nihilists, porn mobsters and Busby Berkeley beauties.",  # NOQA
    year="1998",
    director="Joel Coen, Ethan Coen",
    genre=genre6,
    user_id=user_id
    )
session.add(movie23)
session.commit()

movie24 = Movie(
    title="Dumb and Dumber",
    description="Dumb and Dumber is a 1994 American comedy film starring Jim Carrey and Jeff Daniels. It was written by the Farrelly brothers and Bennett Yellin, and is the Farrelly brothers' directorial debut.",  # NOQA
    year="1994",
    director="Peter Farrelly, Bobby Farrelly",
    genre=genre6,
    user_id=user_id
    )
session.add(movie24)
session.commit()
