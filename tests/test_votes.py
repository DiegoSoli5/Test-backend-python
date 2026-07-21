
import pytest
from app import models

@pytest.fixture()
def  test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[0].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()
    session.refresh(new_vote)
    return new_vote

def test_vote_on_post(autClient, test_posts):
    res = autClient.post("/vote/", json={"post_id": test_posts[2].id, "dir": 1})
    assert res.status_code == 201
    assert res.json().get('message') == 'successfully added vote'
    
def test_vote_on_post_twice(autClient, test_posts, test_vote):
    res = autClient.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 409

def test_delete_vote(autClient, test_posts, test_vote):
    res = autClient.post("/vote/", json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 201
    assert res.json().get('message') == 'successfully deleted vote'

def test_delete_vote_not_exist(autClient, test_posts):
    res = autClient.post("/vote/", json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 404

def test_vote_post_not_exist(autClient, test_posts):
    res = autClient.post("/vote/", json={"post_id": 999999, "dir": 1})
    assert res.status_code == 404

def test_unauthorized_user_vote(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401
    assert res.json().get('detail') == 'Not authenticated'