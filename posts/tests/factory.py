import pytz
from faker import Faker

from posts.models import Post


fake = Faker()


def create_post():
    p = Post(
        title=fake.catch_phrase(),
        contents=fake.text(),
        date=fake.date_time(tzinfo=pytz.utc),
        published=True,
    )
    p.save()
    return p


def create_edited_post():
    edited_date = fake.date_time_between(
            start_date="-3d",
            end_date="-2h",
            tzinfo=pytz.utc)
    created_date = fake.date_time_between(
            start_date="-2y",
            end_date="-4d",
            tzinfo=pytz.utc)
    p = Post(
        title=fake.catch_phrase(),
        contents=fake.text(),
        date=created_date,
        last_edited_date=edited_date,
        published=True,
    )
    p.save()
    return p


def create_unpublished_post():
        p = Post(
            title=fake.catch_phrase(),
            contents=fake.text(),
            date=fake.date_time(tzinfo=pytz.utc),
            published=False,
        )
        p.save()
        return p
