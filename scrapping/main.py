from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from declarations import Event, Base
from events_crawler import get_latest_events
 
engine = create_engine('sqlite:///events_db.sqlite')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Übung 4
events = get_latest_events()

for event in events:
    # Ü6 Duplikats Eliminierung
    select = session.select().where(Event.identifier == event['identifier'])
    existing_rows = conn.execute(s)

    if (len(existing_rows) == 0):
        session.add(Event(
            name = event['name'],
            location = event['location'],
            link = event['link'],
            short = event['short'],
            date = event['date'],
            source = event['source'],
            identifier = event['identifier']
        ))

session.commit()