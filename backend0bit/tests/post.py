from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from backend0bit.models import Post
from rest_framework_jwt import utils
from django.contrib.auth.models import User


class PostTests(APITestCase):
    list_url_name = 'post-list'
    detail_url_name = 'post-detail'
    test_title = "This is a random title"
    test_contents = "This is not a random text"
    test_post = {
            "title": test_title,
            "contents": test_contents
        }

    def setUp(self):
        self.post0 = Post.objects.create(title="Title0", contents="TestTestTest")
        self.post1 = Post.objects.create(title="Some title", contents="Lorem ipsum")
        user = User.objects.create_user("username", "password1")
        payload = utils.jwt_payload_handler(user)
        self.auth_token = utils.jwt_encode_handler(payload)

    def test_list_posts(self):
        url = reverse(self.list_url_name)
        response = self.client.get(url)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, self.json_post_set_representation([self.post0, self.post1]).encode())

    def test_post_details(self):
        url = reverse(self.detail_url_name, args=[self.post1.id])
        response = self.client.get(url)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, self.json_post_representation(self.post1).encode())

    def test_cant_crete_new_post_when_anonymous(self):
        url = reverse(self.list_url_name)
        response = self.client.post(url, self.test_post)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(2, len(Post.objects.all()))

    def test_cant_crete_new_post_with_bad_token(self):
        url = reverse(self.list_url_name)
        auth = 'JWT {0}'.format("BAD" + self.auth_token)
        response = self.client.post(url, self.test_post, HTTP_AUTHORIZATION=auth)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(2, len(Post.objects.all()))

    def test_can_crete_new_post_when_authenticated(self):
        url = reverse(self.list_url_name)
        auth = 'JWT {0}'.format(self.auth_token)
        response = self.client.post(url, self.test_post, HTTP_AUTHORIZATION=auth)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, len(Post.objects.all()))

        post = Post.objects.filter(title=self.test_title)

        self.assertEqual(1, len(post))
        self.assertEqual(post[0].title, self.test_title)
        self.assertEqual(post[0].contents, self.test_contents)

    def test_can_update_post_when_authenticated(self):
        url = reverse(self.detail_url_name, args=[self.post0.id])
        auth = 'JWT {0}'.format(self.auth_token)
        response = self.client.patch(url, self.test_post, HTTP_AUTHORIZATION=auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(Post.objects.all()))
        post = Post.objects.filter(title=self.test_title)
        self.assertEqual(1, len(post))
        self.assertEqual(self.test_title, post[0].title)
        self.assertEqual(self.test_contents, post[0].contents)

    def test_cant_update_post_when_anonymous(self):
        url = reverse(self.detail_url_name, args=[self.post0.id])
        response = self.client.patch(url, self.test_post)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(2, len(Post.objects.all()))
        self.assertEqual(0, len(Post.objects.filter(title=self.test_title)))
        self.assertEqual(0, len(Post.objects.filter(contents=self.test_contents)))

    def test_cant_update_post_with_bad_token(self):
        url = reverse(self.detail_url_name, args=[self.post0.id])
        auth = 'JWT {0}'.format("BAD" + self.auth_token)
        response = self.client.patch(url, self.test_post, HTTP_AUTHORIZATION=auth)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(2, len(Post.objects.all()))
        self.assertEqual(0, len(Post.objects.filter(title=self.test_title)))
        self.assertEqual(0, len(Post.objects.filter(contents=self.test_contents)))

    @classmethod
    def json_post_set_representation(cls, items):
        result = '['
        for item in items:
            result += cls.json_post_representation(item) + ','

        result = result[:-1]  # remove last ','
        result += ']'
        return result

    @classmethod
    def json_post_representation(cls, post):
        return '{"id":' + str(post.id) + ',"title":"' + post.title + '","contents":"' \
               + post.contents + '","date":"' + cls.print_date_like_API(post.date) + '"}'

    @classmethod
    def print_date_like_API(cls, date):
        return date.isoformat()[:-6] + 'Z'
