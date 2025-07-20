import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

# Use an in-memory SQLite for tests.
test_db = SqliteDatabase(":memory:")


class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

    def test_timeline_post(self):
        # Create 2 timeline posts.
        first_post = TimelinePost.create(
            name="John Doe", email="john@example.com", content="Hello world, I'm John!"
        )
        assert first_post.id == 1
        second_post = TimelinePost.create(
            name="Jane Doe", email="jane@example.com", content="Hello world, I'm Jane!"
        )
        assert second_post.id == 2

        # Get all timeline posts
        posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())

        # Convert to list for easier testing
        posts_list = list(posts)

        # Assert we have exactly 2 posts
        assert len(posts_list) == 2

        # Since posts are ordered by created_at desc, Jane's post should be first (created second)
        # and John's post should be second (created first)
        assert posts_list[0].name == "Jane Doe"
        assert posts_list[0].email == "jane@example.com"
        assert posts_list[0].content == "Hello world, I'm Jane!"
        assert posts_list[0].id == 2

        assert posts_list[1].name == "John Doe"
        assert posts_list[1].email == "john@example.com"
        assert posts_list[1].content == "Hello world, I'm John!"
        assert posts_list[1].id == 1
