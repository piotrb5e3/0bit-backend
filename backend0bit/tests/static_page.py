from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from backend0bit.models import StaticPage
from rest_framework_jwt import utils
from django.contrib.auth.models import User


class StaticPageTests(APITestCase):
    list_url_name = 'staticpage-list'
    detail_url_name = 'staticpage-detail'
    test_title = "This is a somewhatrandom title"
    test_contents = "This is not a random text. I've seen it somewhere"
    test_url = "beeps"
    test_page = {
            "title": test_title,
            "contents": test_contents,
            "url": test_url
        }

    def setUp(self):
        self.page0 = StaticPage.objects.create(title="Title17", contents="Test1 Test Test", url="t17")
        self.page1 = StaticPage.objects.create(title="Some title x2", contents="Lorem ipsum 32", url="stx2")
        user = User.objects.create_user("username__0", "password13")
        payload = utils.jwt_payload_handler(user)
        self.auth_token = utils.jwt_encode_handler(payload)

    def test_list_static_pages(self):
        url = reverse(self.list_url_name)
        response = self.client.get(url)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, self.json_static_page_set_representation([self.page0, self.page1]).encode())

    def test_static_page_details(self):
        url = reverse(self.detail_url_name, args=[self.page1.id])
        response = self.client.get(url)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, self.json_static_page_representation(self.page1).encode())

    def test_cant_crete_new_static_page_when_anonymous(self):
        url = reverse(self.list_url_name)
        response = self.client.post(url, self.test_page)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(2, len(StaticPage.objects.all()))

    def test_cant_crete_new_static_page_with_bad_token(self):
        url = reverse(self.list_url_name)
        auth = 'JWT {0}'.format("BAD" + self.auth_token)
        response = self.client.post(url, self.test_page, HTTP_AUTHORIZATION=auth)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(2, len(StaticPage.objects.all()))

    def test_can_crete_new_static_page_when_authenticated(self):
        url = reverse(self.list_url_name)
        auth = 'JWT {0}'.format(self.auth_token)
        response = self.client.post(url, self.test_page, HTTP_AUTHORIZATION=auth)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, len(StaticPage.objects.all()))

        page = StaticPage.objects.filter(title=self.test_title)

        self.assertEqual(1, len(page))
        self.assertEqual(self.test_title, page[0].title)
        self.assertEqual(self.test_contents, page[0].contents)
        self.assertEqual(self.test_url, page[0].url)

    def test_can_update_static_page_when_authenticated(self):
        url = reverse(self.detail_url_name, args=[self.page0.id])
        auth = 'JWT {0}'.format(self.auth_token)
        response = self.client.patch(url, self.test_page, HTTP_AUTHORIZATION=auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(StaticPage.objects.all()))
        page = StaticPage.objects.filter(title=self.test_title)
        self.assertEqual(1, len(page))
        self.assertEqual(self.test_title, page[0].title)
        self.assertEqual(self.test_contents, page[0].contents)

    def test_cant_update_static_page_when_anonymous(self):
        url = reverse(self.detail_url_name, args=[self.page0.id])
        response = self.client.patch(url, self.test_page)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(2, len(StaticPage.objects.all()))
        self.assertEqual(0, len(StaticPage.objects.filter(title=self.test_title)))
        self.assertEqual(0, len(StaticPage.objects.filter(contents=self.test_contents)))

    def test_cant_update_static_page_with_bad_token(self):
        url = reverse(self.detail_url_name, args=[self.page0.id])
        auth = 'JWT {0}'.format("BAD" + self.auth_token)
        response = self.client.patch(url, self.test_page, HTTP_AUTHORIZATION=auth)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(2, len(StaticPage.objects.all()))
        self.assertEqual(0, len(StaticPage.objects.filter(title=self.test_title)))
        self.assertEqual(0, len(StaticPage.objects.filter(contents=self.test_contents)))

    def test_can_find_static_page_by_url(self):
        url = reverse(self.list_url_name)
        response = self.client.get(url + '?url=' + self.page0.url)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, self.json_static_page_set_representation([self.page0]).encode())

    @classmethod
    def json_static_page_set_representation(cls, items):
        result = '['
        for item in items:
            result += cls.json_static_page_representation(item) + ','

        result = result[:-1]  # remove last ','
        result += ']'
        return result

    @classmethod
    def json_static_page_representation(cls, page):
        return '{"id":' + str(page.id) + ',"title":"' + page.title + '","url":"' \
               + page.url + '","contents":"' + page.contents + '"}'
