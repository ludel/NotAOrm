import os
import unittest

import notaorm
from notaorm.datatype import Int, Varchar, ForeignKey
from notaorm.table import Table
from tests.sql_requests import CREATE_TABLES, GENERATE_DATA

notaorm.database = 'test.db'


class TestChange(unittest.TestCase):
    site = Table(name='site', rows=(
        Int('id', primary_key=True),
        Varchar('url', length=255),
        Int('visitor')
    ))
    user = Table(name='user', rows=(
        Int('id', primary_key=True, not_null=True),
        Varchar('name'),
        ForeignKey('site', reference=site)
    ))
    webmaster = Table(name='webmaster', rows=(
        Int('id', primary_key=True, not_null=True),
        Varchar('email'),
        ForeignKey('user', reference=user),
    ))

    @classmethod
    def setUpClass(cls):
        cls.site.change._conn.executescript(CREATE_TABLES)

    def setUp(self):
        self.site.change._conn.executescript(GENERATE_DATA)
        self.site.change._conn.commit()

    def test_all(self):
        self.assertIsNotNone(self.site.show.all())

    def test_get(self):
        test_url = self.site.show.get(self.site.url == 'test.com')
        self.assertEqual(test_url.url, 'test.com')

    def test_get_conditional_and(self):
        conditions = (self.site.url == 'aaa.com') & (self.site.visitor == 5) & (self.site.id >= 0)
        site = self.site.show.get(conditions)
        self.assertEqual(site.url, 'aaa.com')
        self.assertEqual(site.visitor, 5)

    def test_get_conditional_or(self):
        conditions = (self.site.url == 'google.com') | (self.site.visitor == 5)
        sites = self.site.show.filter(conditions)
        self.assertEqual(len(list(sites)), 3)

    def test_insert(self):
        self.site.change.insert(url='facebook.com')
        self.assertIsNotNone(self.site.show.get(self.site.url == 'facebook.com'))

    def test_filter(self):
        test_url = self.site.show.filter(self.site.id >= 0)
        self.assertGreater(len(list(test_url)), 1)

    def test_update(self):
        self.site.change.update(self.site.url.like('test.c%'), url='test2.com')
        self.assertIsNone(self.site.show.get(self.site.url == 'test.com'))
        self.assertIsNotNone(self.site.show.get(self.site.url == 'test2.com'))

    def test_delete(self):
        self.site.change.delete(self.site.url == 'test.com', commit=True)
        self.assertIsNone(self.site.show.get(self.site.url == 'test.com'))

    def test_order_by(self):
        latest = self.site.show.filter(self.site.visitor == 5, order_by=self.site.id)
        self.assertEqual(list(latest)[0].url, 'aaa.com')

        first = self.site.show.filter(self.site.visitor == 5, order_by_desc=self.site.id)
        self.assertEqual(list(first)[0].url, 'bbb.com')

    def test_limit(self):
        last = self.site.show.all(limit=1)
        self.assertEqual(len(list(last)), 1)

    def test_group_by(self):
        site = self.site.show.get(
            self.site.url == 'aaa.com',
            self.site.visitor.sum,
            group_by=self.site.url
        )
        self.assertEqual(site.sum_visitor, 20)

        site = self.site.show.get(
            self.site.url == 'aaa.com',
            self.site.visitor.count,
            group_by=self.site.url
        )

        self.assertEqual(site.count_visitor, 2)

    def test_pk(self):
        last_id = self.site.show.last().id
        site = self.site.show.get(self.site.pk == last_id)
        self.assertEqual(site.id, last_id)

    def test_first(self):
        self.assertEqual(self.site.show.first().url, 'test.com')

    def test_last(self):
        self.assertEqual(self.site.show.last().url, 'bbb.com')

    def test_foreign_key(self):
        test_user = self.user.show.get(self.user.name == 'Benoit Dubois')
        test_webmaster = self.webmaster.show.get(self.webmaster.email == 'ben.dubois@test.com')

        linked_user = test_webmaster.user.first()
        self.assertEqual(linked_user.id, test_user.id)
        self.assertEqual(linked_user.name, test_user.name)

        self.assertEqual(linked_user.site.pk, 2)
        self.assertEqual(linked_user.site.first().url, 'google.com')

    def test_math_method(self):
        sum_visitor = self.site.show.get(self.site.url == 'aaa.com', columns=self.site.visitor.sum)
        self.assertEqual(sum_visitor.sum_visitor, 20)

        count_visitor = self.site.show.get(self.site.url == 'aaa.com', columns=self.site.visitor.count)
        self.assertEqual(count_visitor.count_visitor, 2)

        min_visitor = self.site.show.get(self.site.url.start_with('google'), columns=self.site.visitor.min)
        self.assertEqual(min_visitor.min_visitor, 100)

        max_visitor = self.site.show.get(self.site.url.start_with('google'), columns=self.site.visitor.max)
        self.assertEqual(max_visitor.max_visitor, 1000)

        avg_visitor = self.site.show.get(self.site.url == 'aaa.com', columns=self.site.visitor.avg)
        self.assertEqual(avg_visitor.avg_visitor, 10)

        max_all_visitor = self.site.show.first(columns=self.site.visitor.max)
        self.assertEqual(max_all_visitor.max_visitor, 1000)

    @classmethod
    def tearDownClass(cls):
        os.remove(notaorm.database)
