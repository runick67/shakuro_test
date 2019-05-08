from django.contrib import admin

from main_app import models


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'shops')


class BookInstanceInline(admin.TabularInline):
    model = models.BookInstance
    extra = 0


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'instances_count')
    inlines = [BookInstanceInline]


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'shop', 'is_sold')


admin.site.register(models.Publisher, PublisherAdmin)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Shop)
admin.site.register(models.BookInstance, BookInstanceAdmin)
