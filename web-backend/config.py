import os

class Config:
    # Use absolute path for the SQLite database
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, '../data/src/db/tcm.db')}"
    # SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, '../data/src/db-processing/Joined.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    print(f'Config basedir: {basedir}')
    # if not os.path.exists('../data/src/db-processing/Joined.db'):
    #     print(f"Error: Cannot access the database at {'../data/src/db-processing/Joined.db'}")
