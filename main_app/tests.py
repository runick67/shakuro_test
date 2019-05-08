import json
from django.test import Client, TestCase

from main_app.models import Publisher, Book, Shop, BookInstance


class ViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.publisher_0 = Publisher.objects.create(name="O'Reilly")
        self.publisher_0.save()
        self.publisher_1 = Publisher.objects.create(name="Press book")
        self.publisher_1.save()
        self.book_0 = Book.objects.create(title='Learning Python',
                                          publisher=self.publisher_0)
        self.book_0.save()
        self.book_1 = Book.objects.create(title='Learning Django',
                                          publisher=self.publisher_0)
        self.book_1.save()
        self.shop_0 = Shop.objects.create(name='Amazon')
        self.shop_0.save()
        self.shop_1 = Shop.objects.create(name='eBay')
        self.shop_1.save()
        self.shop_2 = Shop.objects.create(name='eBook')
        self.shop_2.save()
        self.bi_0 = BookInstance.objects.create(book=self.book_0,
                                                shop=self.shop_1, is_sold=True)
        self.bi_0.save()
        self.bi_1 = BookInstance.objects.create(book=self.book_0,
                                                shop=self.shop_1, is_sold=True)
        self.bi_1.save()
        self.bi_2 = BookInstance.objects.create(book=self.book_0,
                                                shop=self.shop_1, is_sold=False)
        self.bi_2.save()
        self.bi_3 = BookInstance.objects.create(book=self.book_1,
                                                shop=self.shop_1, is_sold=True)
        self.bi_3.save()
        self.bi_4 = BookInstance.objects.create(book=self.book_1,
                                                shop=self.shop_1, is_sold=False)
        self.bi_4.save()
        self.bi_5 = BookInstance.objects.create(book=self.book_0,
                                                shop=self.shop_0, is_sold=True)
        self.bi_5.save()
        self.bi_6 = BookInstance.objects.create(book=self.book_0,
                                                shop=self.shop_0, is_sold=False)
        self.bi_6.save()
        self.bi_7 = BookInstance.objects.create(book=self.book_0,
                                                shop=self.shop_2, is_sold=False)
        self.bi_7.save()
        self.bi_8 = BookInstance.objects.create(book=self.book_0,
                                                shop=self.shop_2, is_sold=False)
        self.bi_8.save()

    def test_publisher_list(self):
        result = self.client.get('/publishers/').content
        expected = [{"id": self.publisher_0.id, "name": self.publisher_0.name},
                    {"id": self.publisher_1.id, "name": self.publisher_1.name}]
        self.assertEqual(json.loads(result), json.loads(json.dumps(expected)))

    def test_publisher_detail(self):
        result = self.client.get(
            '/publisher/{}/'.format(self.publisher_0.id)).content
        expected = {"shops": [
            {"id": self.shop_1.id, "name": self.shop_1.name, "books_count": 5,
             "books_sold_count": 3, "books_in_stock": [
                {"id": self.book_0.id, "title": self.book_0.title,
                 "copies_in_stock": 1},
                {"id": self.book_1.id, "title": self.book_1.title,
                 "copies_in_stock": 1}]},
            {"id": self.shop_0.id, "name": self.shop_0.name, "books_count": 2,
             "books_sold_count": 1, "books_in_stock": [
                {"id": self.book_0.id, "title": self.book_0.title,
                 "copies_in_stock": 1}]},
            {"id": self.shop_2.id, "name": self.shop_2.name, "books_count": 2,
             "books_sold_count": 0, "books_in_stock": [
                {"id": self.book_0.id, "title": self.book_0.title,
                 "copies_in_stock": 2}]}]}
        self.assertEqual(json.loads(result), json.loads(json.dumps(expected)))

    def test_set_sold_status_for_shop(self):
        data = {"books": [self.bi_2.id, self.bi_4.id, self.bi_6.id]}
        self.client.post('/shop/{}/'.format(self.shop_1.id), data)
        self.assertTrue(BookInstance.objects.get(id=self.bi_2.id).is_sold)
        self.assertTrue(BookInstance.objects.get(id=self.bi_4.id).is_sold)
        self.assertFalse(BookInstance.objects.get(id=self.bi_6.id).is_sold)
