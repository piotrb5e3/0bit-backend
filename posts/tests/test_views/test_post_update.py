import pytz

from datetime import datetime

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_jwt import utils
from django.contrib.auth.models import User

from posts.models import Post

from posts.tests.factory import create_post, create_edited_post


class TestPost(APITestCase):
    list_url_name = 'post-list'
    detail_url_name = 'post-detail'
    test_title = "This is a random title"
    test_contents = "This is not a random text"
    test_post = {
        "title": test_title,
        "contents": test_contents
    }
    auth_token = None
    auth = None
    post0 = None
    post1 = None

    def setUp(self):
        self.post0 = create_post()
        self.post1 = create_edited_post()

        user = User.objects.create_user("username", "password1")
        payload = utils.jwt_payload_handler(user)
        self.auth_token = utils.jwt_encode_handler(payload)
        self.auth = 'JWT {0}'.format(self.auth_token)

    def test_can_update_post_when_authenticated(self):
        url = reverse(self.detail_url_name, args=[self.post0.id])
        response = self.client.patch(url, self.test_post,
                                     HTTP_AUTHORIZATION=self.auth)
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        last_edited_date = Post.objects.get(pk=self.post0.id).last_edited_date

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(Post.objects.all()))
        self.assertIsNotNone(last_edited_date)
        self.assertLess(last_edited_date, now)
        self._assure_changes_successful()

    def _assure_changes_successful(self):
        post = Post.objects.filter(title=self.test_title)
        self.assertEqual(1, len(post))
        self.assertEqual(self.test_title, post[0].title)
        self.assertEqual(self.test_contents, post[0].contents)

    def test_cant_update_post_when_anonymous(self):
        url = reverse(self.detail_url_name, args=[self.post0.id])
        response = self.client.patch(url, self.test_post)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self._assert_unchanged_state()

    def test_cant_update_post_with_bad_token(self):
        url = reverse(self.detail_url_name, args=[self.post0.id])
        response = self.client.patch(url, self.test_post,
                                     HTTP_AUTHORIZATION="BAD TKN")

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self._assert_unchanged_state()

    def _assert_unchanged_state(self):
        self.assertEqual(2, len(Post.objects.all()))
        self.assertEqual(0, len(Post.objects.filter(title=self.test_title)))
        self.assertEqual(
            0,
            Post.objects.filter(contents=self.test_contents).count()
        )
