from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
# import ruslinkers.models

engine = create_engine('sqlite:///ruslinkers-new4.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

import csv
# Generate the dictionary of lists of dictionaries, for diachronic db
diachronic = { }
with open('ruslinkers-dia-1.0.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        modforms = row.split('; ')
        for form in modforms:
            diachronic.setdefault(form, []).append(row)

# def init_db():
#     # import all modules here that might define models so that
#     # they will be registered properly on the metadata.  Otherwise
#     # you will have to import them first before calling init_db()
#     Base.metadata.create_all(bind=engine)