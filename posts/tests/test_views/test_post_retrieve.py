import json

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from posts.tests.factory import (create_post, create_edited_post,
                                 create_unpublished_post)


class TestPostRetrieve(APITestCase):
    list_url_name = 'post-list'
    detail_url_name = 'post-detail'

    post0 = None
    post1 = None
    unpublished_post = None

    def setUp(self):
        self.post0 = create_post()
        self.post1 = create_edited_post()
        self.unpublished_post = create_unpublished_post()

    def test_list_only_published_posts(self):
        url = reverse(self.list_url_name)
        response = self.client.get(url)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.json_post_set_representation([self.post0, self.post1])
        )

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
