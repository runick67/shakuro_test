from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from main_app.models import Publisher, BookInstance, Shop
from main_app.serializers import PublisherSerializer, BookInstanceSerializer


def publisher_list(request):
    """ Show list of all publishers

    :param request: Django HTTP request
    :return: JsonResponse
    """
    if request.method == 'GET':
        publishers = Publisher.objects.all()
        serializer = PublisherSerializer(publishers, many=True)
        return JsonResponse(serializer.data, safe=False)


def set_sold_status_by_book_id(book_id, shop):
    """ Set sold status to True for the book instance

    :param book_id: BookInstance id
    :param shop: Shop
    :return: BookInstance if success or None
    """
    try:
        book_instance = BookInstance.objects.get(
            id=book_id, shop=shop, is_sold=False)
        book_instance.is_sold = True
        book_instance.save()
        return book_instance
    except (ValidationError, ObjectDoesNotExist):
        return None


@csrf_exempt
def shop_details(request, pk):
    """ Handles GET and POST request for the shop.
    GET: Show shop details for the specific shop id.
    POST: Sets books sold status to True for that shop.

    :param request: django HTTP request
    :param pk: Shop id
    :return: JsonResponse
    GET: shop details and list of books for the shop
    POST: list of changed books
    """
    shop = get_object_or_404(Shop, id=pk)
    if request.method == 'GET':
        books_instances = BookInstance.objects.filter(shop=shop)
        serializer = BookInstanceSerializer(books_instances, many=True)
        return JsonResponse({'id': shop.id, 'name': shop.name,
                             'books': serializer.data}, safe=False)
    elif request.method == 'POST':
        data = dict(request.POST) if request.POST else JSONParser().parse(
            request)
        changed_books = filter(lambda book: book, list(map(
            lambda book_id: set_sold_status_by_book_id(book_id, shop),
            data['books'])))
        serializer = BookInstanceSerializer(changed_books, many=True)
        return JsonResponse(serializer.data, safe=False)


def books_details(books_instances):
    """ Forms books list from books instances

    :param books_instances: list of BookInstance
    :return: list of dict
    """
    instances_in_stock = books_instances.filter(is_sold=False)
    return [{'id': book.id, 'title': book.title,
             'copies_in_stock': instances_in_stock.filter(book=book).count()}
            for book in set(instance.book for instance in instances_in_stock)]


def shop_details_for_publisher(publisher, shop):
    """ Returns shop details for the specific publisher

    :param publisher: Publisher
    :param shop: Shop
    :return: shop details dict
    """
    books_instances = BookInstance.objects.filter(
        book__publisher=publisher, shop=shop)
    return {'id': shop.id, 'name': shop.name,
            'books_count': books_instances.count(),
            'books_sold_count': books_instances.filter(is_sold=True).count(),
            'books_in_stock': books_details(books_instances)}


def publisher_detail(request, pk):
    """ Return publisher detail

    :param request: django HTTP request
    :param pk: Publisher id
    :return: JsonResponse
    """
    if request.method == 'GET':
        publisher = get_object_or_404(Publisher, id=pk)
        shops = list(map(lambda shop: shop_details_for_publisher(
            publisher, shop), publisher.shops()))
        shops.sort(key=lambda shop: shop['books_sold_count'], reverse=True)
        return JsonResponse({'shops': shops})
