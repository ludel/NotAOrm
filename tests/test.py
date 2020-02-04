import os
import unittest

from NotAOrm.table import Table


class Test(unittest.TestCase):
    site = Table(table_name="site", table_row=('id', 'url', 'visitor'))

    @classmethod
    def setUpClass(cls):
        cls.site.change._conn.execute("""
            create table site(id integer constraint site_pk primary key autoincrement, visitor integer DEFAULT 0, url TEXT not null); 
        """)

    def setUp(self):
        self.site.change._conn.executescript("""
            insert into site ('url', 'visitor') values ('test.com', 10);
        """)
        self.site.change._conn.commit()

    def test_all(self):
        self.assertIsNotNone(self.site.show.all())

    def test_get(self):
        test_url = self.site.show.get(self.site.url == 'test.com')
        self.assertEqual(test_url.url, 'test.com')

    def test_insert(self):
        self.site.change.insert(url='google.com')
        self.site.change.insert(url='google2.com')
        print(list(self.site.show.filter(self.site.url.like('goo'))))
        self.assertIsNotNone(self.site.show.get(self.site.url == 'google.com'))

    def test_filter(self):
        self.test_insert()
        test_url = self.site.show.filter(self.site.id >= 0)
        self.assertGreater(len(list(test_url)), 1)

    def test_update(self):
        self.site.change.update(self.site.url == 'test.com', url='test2.com')
        self.assertIsNone(self.site.show.get(self.site.url == 'test.com'))
        self.assertIsNotNone(self.site.show.get(self.site.url == 'test2.com'))

    def test_delete(self):
        self.site.change.delete(self.site.url == 'test.com', commit=True)
        self.assertIsNone(self.site.show.get(self.site.url == 'test.com'))

    def test_order_by(self):
        self.site.change.insert(url='aaa.com')
        self.site.change.insert(url="bbb.com")

        latest = self.site.show.filter(self.site.id > 0, order_by=self.site.url)
        self.assertEqual(list(latest)[0].url, 'aaa.com')

    def test_limit(self):
        self.site.change.insert(url='aaa.com')
        self.site.change.insert(url="bbb.com")

        last = self.site.show.all(limit=1)
        self.assertEqual(len(list(last)), 1)

    def test_group_by(self):
        self.site.change.insert(url='aaa.com', visitor=10)
        self.site.change.insert(url="aaa.com", visitor=10)

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

    @classmethod
    def tearDownClass(cls):
        os.remove('db.sqlite')
