"""
URL configuration for bookstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home, name='home'),
    
    path('genre/<int:id>/', views.genre_books, name='genre_books'),
    path('publisher/<int:id>/', views.publisher_books, name='publisher_books'),
  
    path('accounts/login/', views.custom_login, name='login'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('accounts/orders/', views.user_orders, name='user_orders'),
    
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/<int:book_id>/buy/', views.buy_book, name='buy_book'),
    path('books/read/<int:book_id>/', views.read_book, name='read_book'),
    
    path('buy/<int:book_id>/', views.buy_book, name='buy_book'),
    path('orders/pay/<int:order_id>/', views.pay_order, name='pay_order'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    
    path('export_page/', views.export_page, name='export_page'),
    path('export/<str:model_name>/<str:format>/', views.export_data, name='export_data'),
    path('export/book_genre/<str:format>/', views.export_data, {'model_name': 'BooksGenre'}, name='export_books_genre'),
    path('export/author/<str:format>/', views.export_data, {'model_name': 'Author'}, name='export_author'),
    path('export/publisher/<str:format>/', views.export_data, {'model_name': 'Publisher'}, name='export_publisher'),
    path('export/user/<str:format>/', views.export_data, {'model_name': 'User'}, name='export_user'),
    path('export/genre/<str:format>/', views.export_data, {'model_name': 'Genre'}, name='export_genre'),
    
    path('books/purchased/', views.purchased_books, name='purchased_books'),
    path('books/read/<int:book_id>/', views.read_book, name='read_book'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)