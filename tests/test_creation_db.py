import os
import unittest
from datetime import date, datetime
from sqlite3 import IntegrityError

import notaorm
from notaorm.datatype import Int, Varchar, Text, Bool, Date, Datetime, ForeignKey
from notaorm.table import Table

notaorm.database = 'test.db'
date_test = date(2020, 2, 19)


class TestCreationDB(unittest.TestCase):
    site = Table(name='site', rows=(
        Int('id', primary_key=True, not_null=True),
        Varchar('url', length=255, unique=True, not_null=True),
        Text('content', unique=True),
        Int('visitor', default=0),
        Bool('is_open', default=True),
        Date('last_check', default=date_test),
        Datetime('datetime', default='now'),
    ))
    site.create()

    def setUp(self):
        self.site.change.delete(self.site.id > 0, commit=True)

    def test_id(self):
        self.site.change.insert(content='great size', url='test.com')
        self.site.change.insert(content='great size too', url='test2.com')
        first = self.site.show.first()
        self.assertEqual(self.site.show.last().id, first.id + 1)

    def test_not_null(self):
        with self.assertRaisesRegex(IntegrityError, 'NOT NULL constraint failed: site.url'):
            self.site.change.insert(content='great size')

    def test_default(self):
        self.site.change.insert(content='great size', url='test.com')
        site = self.site.show.get(self.site.url == 'test.com')
        self.assertEqual(site.visitor, 0)
        self.assertEqual(site.last_check, date_test)

    def test_unique(self):
        self.site.change.insert(content='great size', url='test.com')
        with self.assertRaisesRegex(IntegrityError, 'UNIQUE constraint failed: site.url'):
            self.site.change.insert(content='great size 2', url='test.com')

    def test_types(self):
        self.site.change.insert(content='great size', url='test.com', visitor=50)
        site = self.site.show.get(self.site.url == 'test.com')

        self.assertIsInstance(site.id, int)
        self.assertIsInstance(site.url, str)
        self.assertIsInstance(site.content, str)
        self.assertIsInstance(site.visitor, int)
        self.assertIsInstance(site.is_open, bool)
        self.assertIsInstance(site.last_check, date)
        self.assertIsInstance(site.datetime, datetime)

    def test_foreign_key(self):
        webmaster = Table(name='webmaster', rows=(
            Int('uid', primary_key=True, not_null=True),
            Varchar('username', unique=True),
            ForeignKey('site', self.site)
        ))
        webmaster.create()
        self.assertTrue(hasattr(webmaster, 'site'))

    @classmethod
    def tearDownClass(cls):
        os.remove(notaorm.database)
