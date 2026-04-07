from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models import Base
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, event # Add event
# ... inside DBClient.__init__ ...

load_dotenv()

class DBClient:
    def __init__(self):
        # sqlite:///./sentinel.db
        url = os.getenv("DATABASE_URL")
        # 'check_same_thread' is required ONLY for SQLite
        self.engine = create_engine(url, connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.engine = create_engine(url, connect_args={"check_same_thread": False})
    # Add this "WAL" listener for SQLite concurrency
        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL") # The magic scaling line
            cursor.execute("PRAGMA synchronous=NORMAL")
            cursor.close()
        
    def get_session(self):
        return self.Session()       

