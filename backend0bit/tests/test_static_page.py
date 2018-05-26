import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_jwt import utils
from django.contrib.auth.models import User

from backend0bit.models import StaticPage


class TestStaticPage(APITestCase):
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
    page0 = None
    page1 = None
    auth_token = None

    def setUp(self):
        self.page0 = StaticPage.objects.create(
            title="Title17",
            contents="Test1 Test Test",
            url="t17")
        self.page1 = StaticPage.objects.create(
            title="Some title x2",
            contents="Lorem ipsum 32",
            url="stx2")
        user = User.objects.create_user("username__0", "password13")
        payload = utils.jwt_payload_handler(user)
        self.auth_token = utils.jwt_encode_handler(payload)

    def test_list_static_pages(self):
        url = reverse(self.list_url_name)
        response = self.client.get(url)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.json_static_page_set_representation([self.page0, self.page1])
        )

    def test_static_page_details(self):
        url = reverse(self.detail_url_name, args=[self.page1.id])
        response = self.client.get(url)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.json_static_page_representation(self.page1)
        )

    def test_cant_crete_new_static_page_when_anonymous(self):
        url = reverse(self.list_url_name)
        response = self.client.post(url, self.test_page)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(2, len(StaticPage.objects.all()))

    def test_cant_crete_new_static_page_with_bad_token(self):
        url = reverse(self.list_url_name)
        auth = 'JWT {0}'.format("BAD" + self.auth_token)
        response = self.client.post(url, self.test_page,
                                    HTTP_AUTHORIZATION=auth)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(2, len(StaticPage.objects.all()))

    def test_can_crete_new_static_page_when_authenticated(self):
        url = reverse(self.list_url_name)
        auth = 'JWT {0}'.format(self.auth_token)
        response = self.client.post(url, self.test_page,
                                    HTTP_AUTHORIZATION=auth)

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
        response = self.client.patch(url, self.test_page,
                                     HTTP_AUTHORIZATION=auth)

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
        self.assertEqual(0,
                         len(StaticPage.objects.filter(title=self.test_title)))
        self.assertEqual(0, len(
            StaticPage.objects.filter(contents=self.test_contents)))

    def test_cant_update_static_page_with_bad_token(self):
        url = reverse(self.detail_url_name, args=[self.page0.id])
        auth = 'JWT {0}'.format("BAD" + self.auth_token)
        response = self.client.patch(url, self.test_page,
                                     HTTP_AUTHORIZATION=auth)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(2, len(StaticPage.objects.all()))
        self.assertEqual(0,
                         len(StaticPage.objects.filter(title=self.test_title)))
        self.assertEqual(0, len(
            StaticPage.objects.filter(contents=self.test_contents)))

    def test_can_find_static_page_by_url(self):
        url = reverse(self.list_url_name)
        response = self.client.get(url + '?url=' + self.page0.url)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         self.json_static_page_set_representation(
                             [self.page0]))

    @classmethod
    def json_static_page_set_representation(cls, items):
        return [cls.json_static_page_representation(item) for item in items]

    @classmethod
    def json_static_page_representation(cls, page):
        return {
            "id": page.id,
            "title": page.title,
            "url": page.url,
            "contents": page.contents,
            "order": page.order,
        }


class TestStaticPageOrdering(APITestCase):
    sp0 = None
    sp1 = None
    sp2 = None

    order0 = 0
    order1 = 0
    order2 = 0

    reorder_url = reverse('reorder-staticpages')
    auth_token = None
    auth = None
    order_data = None

    def setUp(self):
        self.sp0 = StaticPage.objects.create(title="a", url="b", contents="c")
        self.sp1 = StaticPage.objects.create(title="aa", url="bb",
                                             contents="cc")
        self.sp2 = StaticPage.objects.create(title="aaa", url="bbb",
                                             contents="ccc")

        self.order0 = self.sp0.order
        self.order1 = self.sp1.order
        self.order2 = self.sp2.order

        user = User.objects.create_user("username_f", "password_57634533")
        payload = utils.jwt_payload_handler(user)
        self.auth_token = utils.jwt_encode_handler(payload)
        self.auth = 'JWT {0}'.format(self.auth_token)

    def test_correct_default_order(self):
        self._assert_has_initial_order()

    def test_can_reorder(self):
        response = self.client.post(self.reorder_url,
                                    self._wrap_order_list(
                                        [self.sp1.id, self.sp2.id,
                                         self.sp0.id]),
                                    HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        sp0 = StaticPage.objects.get(id=self.sp0.id)
        sp1 = StaticPage.objects.get(id=self.sp1.id)
        sp2 = StaticPage.objects.get(id=self.sp2.id)
        self.assertEqual(2, sp0.order)
        self.assertEqual(0, sp1.order)
        self.assertEqual(1, sp2.order)

    def test_cant_reorder_if_not_authenticated(self):
        response = self.client.post(self.reorder_url,
                                    self._wrap_order_list(
                                        [self.sp1.id, self.sp2.id,
                                         self.sp0.id]))

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self._assert_has_initial_order()

    def test_cant_reorder_if_incorrect_param_number(self):
        response = self.client.post(self.reorder_url,
                                    self._wrap_order_list(
                                        [self.sp1.id, self.sp0.id]),
                                    HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self._assert_has_initial_order()

    def test_cant_reorder_if_not_all_ids_in_order(self):
        response = self.client.post(self.reorder_url,
                                    self._wrap_order_list(
                                        [self.sp1.id, self.sp0.id,
                                         self.sp0.id]),
                                    HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self._assert_has_initial_order()

    def test_cant_reorder_with_non_integer_ids(self):
        response = self.client.post(self.reorder_url,
                                    self._wrap_order_list(
                                        [self.sp1.id, "a", self.sp0.id]),
                                    HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self._assert_has_initial_order()

    def test_cant_reorder_with_bad_json_data(self):
        response = self.client.post(self.reorder_url,
                                    self._wrap_order_list("[ad, 1, 89["),
                                    HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self._assert_has_initial_order()

    def _assert_has_initial_order(self):
        sp0 = StaticPage.objects.get(id=self.sp0.id)
        sp1 = StaticPage.objects.get(id=self.sp1.id)
        sp2 = StaticPage.objects.get(id=self.sp2.id)
        self.assertEqual(self.order0, sp0.order)
        self.assertEqual(self.order1, sp1.order)
        self.assertEqual(self.order2, sp2.order)

    @classmethod
    def _wrap_order_list(cls, order_list):
        return {
            "order": order_list
        }
