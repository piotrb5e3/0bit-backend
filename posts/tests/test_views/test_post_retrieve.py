import json

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework_jwt import utils

from posts.tests.factory import (create_post, create_edited_post,
                                 create_unpublished_post)


class TestPostRetrieve(APITestCase):
    list_url_name = 'post-list'
    detail_url_name = 'post-detail'

    post0 = None
    post1 = None
    unpublished_post = None

    auth_token = None
    auth = None

    def setUp(self):
        self.post0 = create_post()
        self.post1 = create_edited_post()
        self.unpublished_post = create_unpublished_post()

        user = User.objects.create_user("username", "password1")
        payload = utils.jwt_payload_handler(user)
        self.auth_token = utils.jwt_encode_handler(payload)
        self.auth = 'JWT {0}'.format(self.auth_token)

    def test_list_only_published_posts_when_anonymous(self):
        url = reverse(self.list_url_name)
        response = self.client.get(url)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.json_post_set_representation([self.post0, self.post1]))

    def test_list_all_posts_when_authenticated(self):
        url = reverse(self.list_url_name)
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.json_post_set_representation(
                [self.post0, self.post1, self.unpublished_post]))

    def test_post_details(self):
        url = reverse(self.detail_url_name, args=[self.post1.id])
        response = self.client.get(url)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.json_post_representation(self.post1)
        )

    def test_cant_retrieve_unpublished_post_details(self):
        url = reverse(self.detail_url_name, args=[self.unpublished_post.id])
        response = self.client.get(url)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_retrieve_unpublished_post_details_when_authorised(self):
        url = reverse(self.detail_url_name, args=[self.unpublished_post.id])
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.json_post_representation(self.unpublished_post))

    def test_can_retrieve_filtered_by_is_published_when_authenticated(self):
        url = reverse(self.list_url_name)
        response = self.client.get(
            url,
            {'published': False},
            HTTP_AUTHORIZATION=self.auth)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.json_post_set_representation([self.unpublished_post]))

    @classmethod
    def json_post_set_representation(cls, items):
        return [cls.json_post_representation(item) for item in items]

    @classmethod
    def json_post_representation(cls, post):
        return {
            "id": post.id,
            "title": post.title,
            "contents": post.contents,
            "date": cls.print_date_like_API(post.date),
            "lastEditedDate": cls.print_date_like_API(post.last_edited_date),
            "published": post.published,
        }

    @classmethod
    def print_date_like_API(cls, date):
        if date is not None:
            return date.isoformat()[:-6] + 'Z'
        else:
            return None
