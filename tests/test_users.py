from app import schemas
import jwt
from app.config import settings


def test_root(client):
    res = client.get("/")
    assert res.json().get('Hello') == 'server is running'
    assert res.status_code == 200
    
def test_create_user(client):
    res = client.post("/users/", json={"email":"johndoe@email.com", "password":"password123"})
    
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "johndoe@email.com"
    assert res.status_code == 201
    
def test_login_user(client, test_user):
    res = client.post('/login', data={'username':test_user["email"], 'password': test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id:str = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
    
def test_incorrect_login(test_user, client):
    res = client.post('/login', data={'username':test_user["email"], 'password': 'wrongpass'})
    
    assert res.status_code == 403
    assert res.json().get('detail') == 'Invalid Credentials'