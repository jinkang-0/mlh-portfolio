import unittest
import os

os.environ["TESTING"] = "true"

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Jinkang Fang</title>" in html

        # Test that key sections are present
        assert "About Me" in html
        assert "Work Experience" in html
        assert "Education" in html

        # Test that personal information is displayed
        assert "full-stack developer" in html
        assert "University of California, Berkeley" in html

        # Test that work experience is shown
        assert "Software Engineer Intern" in html
        assert "Moody&#39;s Analytics" in html

        # Test navigation is present
        assert "Home" in html
        assert "Hobbies" in html
        assert "Timeline" in html

    def test_timeline_api_get_empty(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

    def test_timeline_api_post(self):
        # Test POST request to create a new timeline post
        post_data = {
            "name": "Test User",
            "email": "test@example.com",
            "content": "This is a test post!",
        }
        response = self.client.post("/api/timeline_post", data=post_data)
        assert response.status_code == 200
        assert response.is_json

        # Check that the response contains the created post data
        json = response.get_json()
        assert json["name"] == "Test User"
        assert json["email"] == "test@example.com"
        assert json["content"] == "This is a test post!"
        assert "id" in json
        assert "created_at" in json

    def test_timeline_api_get_with_posts(self):
        # First create a post
        post_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "content": "Hello from John!",
        }
        self.client.post("/api/timeline_post", data=post_data)

        # Create another post
        post_data2 = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "content": "Hello from Jane!",
        }
        self.client.post("/api/timeline_post", data=post_data2)

        # Now test GET request
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json

        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 2

        # Posts should be ordered by created_at desc (Jane's post first)
        posts = json["timeline_posts"]
        assert posts[0]["name"] == "Jane Doe"
        assert posts[0]["email"] == "jane@example.com"
        assert posts[1]["name"] == "John Doe"
        assert posts[1]["email"] == "john@example.com"

    def test_timeline_page(self):
        # Test the timeline page renders correctly when empty
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        # Check page title and content
        assert "<title>Jinkang Fang | Timeline</title>" in html
        assert "Add Post" in html
        assert "Timeline" in html

        # Check form elements are present
        assert '<form id="timeline-form">' in html
        assert 'name="name"' in html
        assert 'name="email"' in html
        assert 'name="content"' in html
        assert 'type="submit"' in html

    def test_timeline_page_with_posts(self):
        # First create some posts via API
        post_data1 = {
            "name": "Alice Smith",
            "email": "alice@example.com",
            "content": "First timeline post!",
        }
        self.client.post("/api/timeline_post", data=post_data1)

        post_data2 = {
            "name": "Bob Johnson",
            "email": "bob@example.com",
            "content": "Second timeline post!",
        }
        self.client.post("/api/timeline_post", data=post_data2)

        # Now test the timeline page displays the posts
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        # Check that both posts are displayed
        assert "Alice Smith" in html
        assert "alice@example.com" in html
        assert "First timeline post!" in html

        assert "Bob Johnson" in html
        assert "bob@example.com" in html
        assert "Second timeline post!" in html

        # Check post structure elements
        assert 'class="post"' in html
        assert 'class="post-header"' in html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com", "content": "Hello world, I'm John!"},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "john@example.com", "content": ""},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello world, I'm John!",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
