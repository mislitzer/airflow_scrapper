from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from declarations import Event, Base
from events_crawler_extended import get_latest_events_extended
 
engine = create_engine('sqlite:///events_db.sqlite')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Übung 5
events = get_latest_events_extended()

for event in events:
    session.add(Event(
        name = event['name'],
        location = event['location'],
        link = event['link'],
        short = '',
        date = event['date'],
        source = event['source'],
        identifier = event['identifier']
    ))

session.commit()