import uuid
from django.db import models


class Publisher(models.Model):

    name = models.CharField(max_length=200)

    def shops(self):
        """ Returns list of shops selling at least one book of that publisher

        :return: list of Shop
        """
        return Shop.objects.filter(
            bookinstance__book__publisher=self).distinct()

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


class Book(models.Model):

    title = models.CharField(max_length=200)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL,
                                  null=True)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{} ({})'.format(self.title, self.publisher)

    def instances_count(self):
        """ Returns book instances count

        :return: Book instances count
        """
        return self.bookinstance_set.count()


class Shop(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    is_sold = models.BooleanField()

    def title(self):
        """ Returns book title

        :return: Book title
        """
        return self.book.title

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{} {}'.format(self.id, self.book.title)
