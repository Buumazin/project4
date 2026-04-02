from db.models import Base
from db.init import get_database_engine

def init_database():
    """Initialize database and create tables"""
    engine = get_database_engine()
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
    return engine
    engine = create_engine(database_url, echo=False)

    # Drop all tables
    Base.metadata.drop_all(engine)
    # Create all tables
    Base.metadata.create_all(engine)

    print("Database reset successfully")
    return engine