
import pytest
from app import schemas


def test_get_all_post(client, test_posts):
    res = client.get("/posts/")
    
    def validate(post):
        return schemas.PostWithVotes(**post)
    post_map = list(map(validate, res.json()))
    print(post_map)
    assert res.status_code == 200
    assert len(post_map) == len(test_posts)
    # el .post.id es para acceder al id del post dentro del objeto PostWithVotes, ya que este objeto tiene un atributo Post que es el post en sí
    assert post_map[0].Post.id == test_posts[0].id


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    assert res.json().get('detail') == 'Not authenticated'

def test_get_one_post_not_exist(autClient):
    res = autClient.get(f"/posts/999999")
    assert res.status_code == 404
    
def test_get_one_post(autClient, test_posts):
    res = autClient.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostWithVotes(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    
@pytest.mark.parametrize("title, content, published", [
    ("Test Post 1", "This is the content of test post 1", True),
    ("Test Post 2", "This is the content of test post 2", False),
    ("Test Post 3", "This is the content of test post 3", True)
])
def test_create_post(autClient, title, content, published):
    res = autClient.post("/posts/", json={"title": title, "content": content, "published": published})
    post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.published == published

def test_create_post_default_published_true(autClient):
    res = autClient.post("/posts/", json={"title": "Test Post", "content": "This is the content of the test post"})
    post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert post.title == "Test Post"
    assert post.content == "This is the content of the test post"
    assert post.published == True

def test_unauthorized_user_create_post(client ):
    res = client.post("/posts/", json={"title":"Test Post", "content":"This is the content of the test post"})
    assert res.status_code == 401
    assert res.json().get('detail') == 'Not authenticated'
    
def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    assert res.json().get('detail') == 'Not authenticated'
    
def test_delete_post_success(autClient, test_posts):
    res = autClient.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_not_exist(autClient):
    res = autClient.delete(f"/posts/999999")
    assert res.status_code == 404
    assert res.json().get('detail') == 'post not found'

def test_delete_post_not_owner(autClient, test_posts):
    res = autClient.delete(f"/posts/{test_posts[2].id}")
    assert res.status_code == 403
    assert res.json().get('detail') == 'Not authorized to perform requested action'

def test_update_post_success(autClient, test_posts):
    res = autClient.put(f"/posts/{test_posts[0].id}", json={"title":"Updated Title", "content":"Updated Content", "published":False})
    post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert post.title == "Updated Title"
    assert post.content == "Updated Content"
    assert post.published == False

def test_update_other_user_post(autClient, test_posts):
    res = autClient.put(f"/posts/{test_posts[2].id}", json={"title":"Updated Title", "content":"Updated Content", "published":False})
    assert res.status_code == 403
    assert res.json().get('detail') == 'Not authorized to perform requested action'

def test_update_post_not_exist(autClient):
    res = autClient.put(f"/posts/999999", json={"title":"Updated Title", "content":"Updated Content", "published":False})
    assert res.status_code == 404
    assert res.json().get('detail') == 'post not found'

def test_unauthorized_user_update_post(client, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}", json={"title":"Updated Title", "content":"Updated Content", "published":False})
    assert res.status_code == 401
    assert res.json().get('detail') == 'Not authenticated'
