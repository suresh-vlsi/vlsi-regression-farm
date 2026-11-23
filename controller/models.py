import os
from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True)
    run_id = Column(String, index=True)
    test = Column(String, index=True)
    seed = Column(Integer)
    status = Column(String)
    passed = Column(Integer)
    failed = Column(Integer)
    duration_s = Column(Float)
    error_signature = Column(String)
    commit = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


def get_session():
    url = os.environ.get("DATABASE_URL", "sqlite:///./local.db")
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
