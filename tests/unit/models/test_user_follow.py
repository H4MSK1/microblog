"""
...
"""
# pylint: disable=redefined-outer-name
from datetime import datetime, timedelta
from app.models import User, Post
from app import db


def test_following(test_app):  # pylint: disable=unused-argument
    """
    DS
    """
    user1 = User(username='john', email='john@example.com')
    user2 = User(username='susan', email='susan@example.com')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    assert user1.followed.all() == []
    assert user1.followers.all() == []

    user1.follow(user2)
    db.session.commit()

    assert user1.is_following(user2) is True
    assert user1.followed.count() == 1
    assert user1.followed.first().username == 'susan'
    assert user2.followers.count() == 1
    assert user2.followers.first().username == 'john'

    user1.unfollow(user2)
    db.session.commit()

    assert user1.is_following(user2) is False
    assert user1.followed.count() == 0
    assert user2.followers.count() == 0


def test_follow_post(test_app):  # pylint: disable=unused-argument
    """
    DS
    """
    user1 = User(username='john', email='john@example.com')
    user2 = User(username='susan', email='susan@example.com')
    user3 = User(username='mary', email='mary@example.com')
    user4 = User(username='david', email='david@example.com')

    db.session.add_all([user1, user2, user3, user4])

    now = datetime.utcnow()

    # create four posts
    now = datetime.utcnow()
    post1 = Post(body="post from john", author=user1,
                 timestamp=now + timedelta(seconds=1))
    post2 = Post(body="post from susan", author=user2,
                 timestamp=now + timedelta(seconds=4))
    post3 = Post(body="post from mary", author=user3,
                 timestamp=now + timedelta(seconds=3))
    post4 = Post(body="post from david", author=user4,
                 timestamp=now + timedelta(seconds=2))
    db.session.add_all([post1, post2, post3, post4])
    db.session.commit()

    # setup the followers
    user1.follow(user2)  # john follows susan
    user1.follow(user4)  # john follows david
    user2.follow(user3)  # susan follows mary
    user3.follow(user4)  # mary follows david
    db.session.commit()

    # check the followed posts of each user
    f1 = user1.followed_posts().all()
    f2 = user2.followed_posts().all()
    f3 = user3.followed_posts().all()
    f4 = user4.followed_posts().all()

    assert f1 == [post2, post4, post1]
    assert f2 == [post2, post3]
    assert f3 == [post3, post4]
    assert f4 == [post4]
