from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.oauth2 import create_access_token
from app import models

from app.database import get_db, Base


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
# engine connects our code to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# session allow us to execute sql queries and get results
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user2(client):
    user_data = {"email":"janedoe@email.com","password":"password123"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {"email":"johndoe@email.com","password":"password123"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user["id"]})

@pytest.fixture
def autClient(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f'bearer {token}'
    }
    
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    post_data = [
        {"title": "Test Post 1", "content": "This is the content of test post 1", "user_id": test_user["id"]},
        {"title": "Test Post 2", "content": "This is the content of test post 2", "user_id": test_user["id"]},
        {"title": "Test Post 3", "content": "This is the content of test post 3", "user_id": test_user2["id"]}
    ]
    
    def create_post_model(post):
        return models.Post(**post)
    posts = list(map(create_post_model, post_data))
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).order_by(models.Post.id).all()
    return posts