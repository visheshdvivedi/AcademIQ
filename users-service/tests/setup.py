import os
import pytest
import sqlalchemy
import sqlalchemy.events

from main import app
from utils.database import get_db, Base

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# connect to test database
SQLALCHEMY_TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create tables once
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture()
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)

    nested = connection.begin_nested()

    @sqlalchemy.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]