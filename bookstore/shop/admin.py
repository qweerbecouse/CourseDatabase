from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Author, Publisher, Genre, Book, BooksGenre, Order

admin.site.register(User)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(BooksGenre)
admin.site.register(Order)

admin.site.unregister(Group)