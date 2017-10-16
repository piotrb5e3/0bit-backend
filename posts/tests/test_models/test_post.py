from django.test import TestCase
from posts.models import Post


class TestPost(TestCase):
    list_url_name = 'post-list'
    detail_url_name = 'post-detail'
    test_title = "This is a random title"
    test_contents = "This is not a random text"
    test_post = {
        "title": test_title,
        "contents": test_contents
    }

    def test_can_create_post(self):
        post = Post.objects.create(title=self.test_title,
                                   contents=self.test_contents)
        self.assertEqual(self.test_title, post.title)
        self.assertEqual(self.test_contents, post.contents)
